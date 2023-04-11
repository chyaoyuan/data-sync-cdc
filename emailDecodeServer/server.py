import asyncio
import base64
import hashlib
import json
import quopri
import re
from email import parser
from typing import Union

import nest_asyncio
import uvicorn
from fastapi import FastAPI, Response
from flanker import mime
from loguru import logger
from lxml import etree
from starlette.responses import JSONResponse
from webob.compat import urlparse

from emailDecodeServer.config import Settings
from emailDecodeServer.email_verify import get_re_func
from emailDecodeServer.model import ChannelModel, EmailDecodeServerRequest
from emailDecodeServer.utils.re_util import get_re_result
from emailDecodeServer.utils.time_transform import time_transformer

app = FastAPI(title="邮件接收服务器", description="对邮件进行解码、测试邮件账户是否可用", docs_url="/pig", redoc_url="/pigs")
email_parser = parser.BytesParser()


# https://yun.bjx.com.cn/resume/details?oid=31012939&rnum=533769E1F1A69D9A&rank=1&type=1&dir=0
def channel_verify(html: str) -> (str, str or None):
    # todo
    # City58 = "58.com"
    candidate_link = None
    channel = ChannelModel.Other
    # https://sctrack.sendcloud.net/track/click2
    if re.search("(http|https)://sctrack.sendcloud.net/track/click/.*.html", html):
        candidate_link = get_re_result(re.search("(http|https)://sctrack.sendcloud.net/track/click/.*.html", html))
        channel = ChannelModel.Boss
    elif re.search("(http|https)://sctrack.sendcloud.net/track/click2/.*.html", html):
        candidate_link = get_re_result(re.search("(http|https)://sctrack.sendcloud.net/track/click2/.*.html", html))
        channel = ChannelModel.Boss

    elif re.search(r"(http|https)://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx.*pageCode=\d*", html):
        candidate_link = get_re_result(
            re.search(r"(http|https)://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx.*pageCode=\d*", html))
        channel = ChannelModel.Job51

    elif re.search(r"(http|https)://yun.bjx.com.cn/resume/details?.*dir=\d*", html):
        candidate_link = get_re_result(re.search(r"(http|https)://yun.bjx.com.cn/resume/details?.*dir=\d*", html))
        channel = ChannelModel.BJX

    elif re.search("(http|https)://linktrace.lietou-edm.com/lietou-edmetracetime[0-9]*/EventInterface/map\?[a-zA-Z0-9-=&;]*enc=3[a-zA-Z0-9-=&;]*", html):
        candidate_link = get_re_result(re.search(
            r"(http|https)://linktrace.lietou-edm.com/lietou-edmetracetime[0-9]*/EventInterface/map\?[a-zA-Z0-9-=&;]*enc=3[a-zA-Z0-9-=&;]*",html))
        channel = ChannelModel.LPT

    elif re.search(r"(http|https)://rd6.zhaopin.com/resume/detail\?resumeNumber=[a-zA-Z0-9-=&;%]*", html):
        candidate_link = get_re_result(
            re.search("(http|https)://rd6.zhaopin.com/resume/detail\?resumeNumber=[a-zA-Z0-9-=&;%]*", html))
        channel = ChannelModel.ZhaoPin
    elif re.search("(http|https)://rd6.zhaopin.com/candidate\?.*resumeNumber=[a-zA-Z0-9-=&;%]*", html):
        candidate_link = get_re_result(re.search("(http|https)://rd6.zhaopin.com/candidate\?.*resumeNumber=[a-zA-Z0-9-=&;%]*", html))
        channel = ChannelModel.ZhaoPin
    elif re.search(r"(http|https)://sh\.58\.com/.*\.shtml", html):
        candidate_link = get_re_result(re.search(r"(http|https)://sh\.58\.com/.*\.shtml", html))
        channel = ChannelModel.City58
    return channel, candidate_link.replace("&amp;", "&") if candidate_link else None


def get_html(eml: mime.from_string):
    charset = None
    # 判断是否为单部分
    if eml.content_type.is_singlepart():
        eml_body = eml.body
    else:
        eml_body = ''
        for part in eml.parts:
            # 判断是否是多部分
            if part.content_type.is_multipart():
                eml_body, charset = get_html(part)
            else:
                if part.content_type.main == 'text':
                    eml_body = part.body
    return eml_body, charset


def get_attachment(eml: mime.from_string, ignore_attachment: list) -> list:
    attachment_result = []
    for part in eml.parts:
        # is_inline属性判断不出来是否inline被弃用
        # logger.info(f"{part.detected_file_name}+{bool(part.is_inline)}")
        if not part.content_type.is_multipart():
            name = part.detected_file_name
            # name 有时为空 需要判断name是否存在
            if name and name not in ignore_attachment:
                atta_format = name.split('.')
                atta_format = atta_format[-1] if len(atta_format) >= 2 else None
                attachment_body = None
                if not part.body:
                    attachment_body = None
                elif isinstance(part.body, bytes):
                    attachment_body = base64.b64encode(part.body).decode()
                else:
                    attachment_body = part.body.encode().decode()

                attachment_result.append(
                    {
                        'attachmentName': name,
                        'attachmentFormat': atta_format,
                        'attachmentBody': attachment_body
                    }
                )
    return attachment_result


def get_filename_charset(filename_line: str) -> str or None:
    # =?utf-8?B?55+l6KGM?=
    guess_charset = get_re_result(re.search(r"(?<==\?)[a-zA-Z0-9-]*(?=\?)", filename_line))
    return guess_charset


def get_filename(_filename_line: Union[str, None], filename=None) -> Union[str, None]:
    # QP编码
    # =?utf-8?B?55+l6KGM?=
    # =?UTF-8?B?44CQ5ZSu5ZCO5oqA5pyv5pSv5oyB5bel56iL5biIIHwg5LiK5rW3?= =?UTF-8?B?NS04S+OAkeiigeixquWGmyAy5bm0LnBkZg==?=
    if not _filename_line:
        return None
    title = ''
    for filename_line in _filename_line.split(' '):
        charset = get_filename_charset(filename_line)
        if re.search(r"(?<=\?Q\?)(=[a-fA-F0-9][a-fA-F0-9])*.*(?=\?=)", filename_line):
            filename_encode = get_re_result(re.search("(?<=\?Q\?)(=[a-fA-F0-9][a-fA-F0-9])*.*(?=\?=)", filename_line))
            filename: bytes = quopri.decodestring(filename_encode.encode())
        elif re.search(r"(?<=\?[a-zA-Z0-9-]\?B\?)(=[a-fA-F0-9][a-fA-F0-9])*.*(?=\?=)", filename_line):
            filename_encode = get_re_result(
                re.search(r"(?<=\?[a-zA-Z0-9-]\?B\?)(=[a-fA-F0-9][a-fA-F0-9])*.*(?=\?=)", filename_line))
            filename: bytes = base64.b64decode(filename_encode.decode())
        if filename and charset:
            title = title + filename.decode(encoding=charset)
            logger.info(f"title->{title}")
            return title
    logger.error(f"附件名称解码错误: _filename_line->{_filename_line} name->{title}")
    return _filename_line


def get_attachment_inline(ignore_attachment: list, lines: [bytes]):
    for line in lines:
        # 会把 Content-Type: text/plain; charset=UTF-8弄进来，但这比没有附件名
        if b'Content-Disposition: inline' in line:
            logger.debug(f"Content-Disposition: inline->{line}")
            _filename = get_re_result(re.search("(?<=filename=\").*(?=\")", line.decode()))
            filename = get_filename(_filename)
            # 会把 Content-Type: text/plain; charset=UTF-8弄进来，但这比没有附件名 把这b排除了
            if not filename:
                continue
            ignore_attachment.append(filename)
        elif b'Content-Disposition: attachment' in line:
            logger.debug(f"Content-Disposition: attachment->{line}")
            # 不具有实际用途，仅测试
            pass
    return ignore_attachment


def get_email_from_line(sender_information: str or None):
    if not sender_information:
        return None
    email_address = get_re_result(re.search("(?<=<).*(?=>)", sender_information))
    return email_address


def html_header_replace(html: str or None):
    if not html:
        return None
    return html


def create_email_unique_id(tenant: str, email: str, header_time: str, subject: str):
    _str = f"{tenant}-{email}-{header_time if header_time else 'header-time'}-{subject if subject else 'subject'}".encode()
    obj = hashlib.md5()
    obj.update(_str)
    return obj.hexdigest()


# 手动上传的邮件收件人会有丢失现象
def get_receiver(lines: [bytes]):
    for line in lines:
        line = line.decode().lower().replace(" ", "")
        if line.startswith("to:"):
            receiver = re.search(r'[a-z0-9]+@[a-z,0-9]+.[a-z]+', line)
            if receiver:
                return receiver.group()


@app.post('/v1/emailApplication/Decode/body', description="邮件body解码", tags=['内部接口'])
async def email_decode(receive_body: EmailDecodeServerRequest):
    try:
        ignore_attachment = []
        lines: [bytes] = [base64.b64decode(line.encode(encoding='UTF-8')) for line in receive_body.emailBodyB64]
        email_body: bytes = b'\r\n'.join(lines)
        # 初解码
        eml: mime.from_string = mime.from_string(email_body)
        header_subject = eml.headers.get('Subject')
        header_from = get_email_from_line(eml.headers.get('From'))
        header_to = get_email_from_line(eml.headers.get('To'))

        if not header_to:
            header_to = get_receiver(lines)

        header_time = time_transformer(eml.headers.get('Date'))
        if receive_body.lineAttachmentIgnore:
            ignore_attachment: list = get_attachment_inline(ignore_attachment, lines)
        attachment: [dict] = get_attachment(eml, ignore_attachment)
        html, html_chrset = get_html(eml)

        email_unique_id = create_email_unique_id(receive_body.tenant, header_to, header_time, header_subject)
        channel, candidate_link = channel_verify(html)
        position = location = None
        if header_subject and channel != ChannelModel.Other and html:
            html_xml = etree.HTML(html)
            re_func = get_re_func(channel)
            position, location = re_func(html_xml)
        information = json.dumps({
            "requestUID": receive_body.RequestUID, "sender": header_from, "subject": header_subject,
            "receiveTime": header_time, "emailUniqueId": email_unique_id, "position": position,"location":location}, ensure_ascii=False)
        logger.info(information)
        result = {
            "emailUniqueId": email_unique_id,
            "subject": header_subject,
            "receiveTime": header_time,
            "sender": header_from,
            "receiver": header_to,
            "attachments": attachment,
            "html": html,
            "position": position,
            "location": location,
            "channel": channel,
            "candidateLink": candidate_link,
            "requestUID": receive_body.RequestUID,
        }
        return JSONResponse(result, status_code=200)
    except Exception as e:
        logger.exception(e)
        logger.info(f"requests error, uuid->{receive_body.RequestUID}")
        return JSONResponse({"msg": f"error, reason: {repr(e)}"}, status_code=500)




if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=Settings.server_port)
