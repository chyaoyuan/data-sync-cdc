import re
from typing import Tuple

from loguru import logger
from lxml import etree

from src.main.currency_model.email_receiver_model import ChannelModel, TenantModel
from src.main.channels.email.pull.utils import get_re_result


def Job51Base(html_xml: etree.HTML, position=None, location=None) -> Tuple:
    position_list: list[etree.HTML] = html_xml.xpath('///td[@valign="top"]/text()')
    position_list: list[str] = [""+_ for _ in position_list]
    for index, position in enumerate(position_list):
        if position == '应聘职位：':
            position = position_list[index+1]
            break
    return position, location


def BJXBase(html_xml: etree.HTML, position=None, location=None) -> Tuple:
    position_list: list[etree.HTML] = html_xml.xpath('//td[@style="margin:0;padding:0 10px;font-size:12px;font-weight:normal;font-family:microsoft yahei,Arial, Helvetica, sans-serif;color:#333;text-align:left;white-space:normal;word-wrap:break-word;word-break:break-all;"]/text()')
    position_list: list[str] = ["" + _ for _ in position_list]
    for _position in position_list:
        if '应聘岗位：' in _position:
            position = _position.replace("应聘岗位：", "")
            break
    return position, location


def LPTBase(html_xml: etree.HTML, position=None, location=None) -> Tuple:
    position_list: list[etree.HTML] = html_xml.xpath(
        '//span[@style="color: #FF993C;font-weight: 600; margin: 0 3px;font-family:Helvetica Neue, Helvetica, Arial,PingFang SC, BlinkMacSystemFont, Hiragino Sans GB, Segoe UI, Roboto, sans-serif;"]/text()')
    position_list: list[str] = ["" + _ for _ in position_list]
    for _position in position_list:
        if get_re_result(re.match(r".*\|.*", _position)):
            position = _position
            break
    return position, location


def ZhaoPinBase(html_xml: etree.HTML, position=None, location=None) -> Tuple:
    position_list: list[etree.HTML] = html_xml.xpath('//a[@style="color: #141933;text-decoration : none;"]/text()')
    position_list: list[str] = ["" + _ for _ in position_list]
    position = position_list[0] if position_list else None
    return position, location


def BossBase(html_xml: etree.HTML, position=None, location=None) -> Tuple:
    position_list: list[etree.HTML] = html_xml.xpath(
        '//span[@style="color: #53CAC3;"]/text()')
    position_list: list[str] = ["" + _ for _ in position_list]
    position = position_list[0] if position_list else None
    if position:
        return position, location
    position_list: list[etree.HTML] = html_xml.xpath("//td[@style]/p[@class='MsoNormal']/span[@style]/text()")
    position_list = "".join(position_list).split("\n")
    if len(position_list) < 2:
        return None, None
    position = position_list[1]
    location = re.search("[\u4e00-\u9fa5]+", position_list[2])
    if location:
        location = location.group()
    return position, location


def City58Base(html_xml: etree.HTML, position=None, location=None) -> Tuple:
    position_list: list[etree.HTML] = html_xml.xpath(
        '//a[@style="color:#2255DD;text-decoration:underline;"]/text()')
    position_list: list[str] = ["" + _ for _ in position_list]
    logger.info(position_list)
    for _position in position_list:
        if get_re_result(re.match(r".*\|.*", _position)):
            position = _position
            break
    return position, location


def get_re_func(channel: ChannelModel):
    re_func = {
        # base渠道
        ChannelModel.Job51: Job51Base,
        ChannelModel.BJX: BJXBase,
        ChannelModel.ZhaoPin: ZhaoPinBase,
        ChannelModel.LPT: LPTBase,
        ChannelModel.City58: City58Base,
        ChannelModel.Boss: BossBase,
    }
    func = re_func.get(channel)
    if not func:
        func = re_func.get(channel)
    if not func:
        raise Exception("re config not found")
    return func


if __name__ == '__main__':
    pass

    # 51Job
    # subject_list = [
    #     "ciic 转发: (51job.com)申请贵公司人力资源总监-0003（上海）－张瑶",
    #     "转发：(51job.com)申请贵公司软件测试工程师（成都）－黄嘉园"
    # ]
    # for _subject in subject_list:
    #     print(Job51Base(_subject))

    # 智联招聘
    # subject_list = [
    #     'Fw:软件测试工程师(成都)-游先生',
    #     '行政实习生(成都)-胡女士',
    #     'Fw:(Zhaopin.com) 应聘 行政实习生-成都-彭女士',
    #     'Fw:(Zhaopin.com) 应聘 客服实习生-成都-田女士',
    #     'Fw:Web前端实习生(成都)-林先生- 智联求职者',
    #     'Web前端实习生(成都)-肖先生',
    #     '转发：软件测试工程师(成都)-付先生']
    # for _subject in subject_list:
    #     print(ZhaoPinZhiYuan(_subject))

    # 北极星
    # subject_list = [
    #     "Fw:Fw:转发：(hbfdjob.bjx.com.cn)应聘 锅炉运行 - 山西运城 - 张峰",
    #     "Fw:Fw:转发：(hdjob.bjx.com.cn)应聘 燃机运行 - 江苏 - 周海涛"
    # ]
    # for _subject in subject_list:
    #     print(BJXBase(_subject))

    # 猎聘
    # subject_list = [
    #         'Fw:【销售经理-华中区_青岛】 张先生_来自猎聘的候选人',
    #         'Fw:【运维工程师_成都】 谢先生_来自猎聘的候选人',
    #         'Fw:【售前及实施顾问-华南区_长沙】 徐斯涵_来自猎聘的候选人',
    #         'Fw:【web前端实习生_成都】 王雨航_来自猎聘的候选人',
    #         '【测试岗位_上海-浦东新区】 唐凯峰_来自猎聘的候选人',
    #         '【Android BSP软件开发助理工程师_上海】 周银_来自猎聘的候选人'
    # ]
    # for _subject in subject_list:
    #     print(LPTBase(_subject))

    # Boss直聘
    # subject_list = [
    #     "Fw:Fw:Fw:赫敏 | 4年，应聘 产品经理 | 上海15-25K【BOSS直聘】",
    #     "Fw:转发：罗思维 | 2年，应聘 软件测试工程师 | 成都6-8K【BOSS直聘】",
    #     "Fw:Fw:Fw:杨晴 | 20年应届生，应聘 新媒体运营 | 上海10-15K【BOSS直聘】"
    # ]
    # for _subject in subject_list:
    #     print(BossBase(_subject))

    # 58
    # subject_list = ['Fw:(58.com)应聘贵公司高薪快递员-上海 奉贤 金汇-龚佳乐']
    # for _subject in subject_list:
    #     print(City58Base(_subject))