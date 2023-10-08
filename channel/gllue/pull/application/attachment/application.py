import base64
from cgi import parse_header
from typing import Optional, Literal, List, Union
from urllib.parse import unquote, urlencode
from datetime import datetime
from channel.gllue.pull.application.schema.application import GleSchema


class GleAttachment(GleSchema):
    # 假定所有实体都有附件
    entityType: str = "file".lower()

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    async def get_attachment(self, attachments_ids: Union[str, list], entity: Optional[dict] = None):
        attachments_ids = ",".join(attachments_ids) if isinstance(attachments_ids, list) else attachments_ids
        # attachments_ids = '33,34,35' assert
        attachments_info, status = await self.async_session.get(
            url=self.settings.get_entity_url.format(entityType=self.entityType),
            ssl=False,
            params={
                "fields": "attachment",
                "gql": f"id__s={attachments_ids}"},
            func=self.request_response_callback)
        if entity:
            entity["mesoorExtraAttachments"] = attachments_info['result']["attachment"]

        for attachment in entity["mesoorExtraAttachments"]:
            # {
            #      "dateAdded": "2023-09-20 22:11:43",
            #      "real_preview_path": "fsgtest/candidate/2023-09/preview/65ecc133-1f02-4872-bba6-37677e4e9890.pdf",
            #      "ext": "txt",
            #      "uuidname": "65ecc133-1f02-4872-bba6-37677e4e9890",
            #      "id": 824,
            #      "type": "candidate",
            #      "__name__": null,
            #      "__oss_url": "/rest/v2/attachment/preview/65ecc133-1f02-4872-bba6-37677e4e9890",
            #      "__download_oss_url": "/rest/v2/attachment/download/65ecc133-1f02-4872-bba6-37677e4e9890",
            #      "__preview_to_pdf": true
            # }
            con, headers = await self.async_session.get(
                url=attachment["__download_oss_url"],
                ssl=False,
                func=self.request_file_response_callback,
            )
            _, params = parse_header(headers.get("Content-Disposition"))
            filename = unquote(params.get('filename'))

            # with open("xxx.doc", "wb") as f:
            #     f.write(con)
            attachment["fileName"] = filename
            attachment["fileContent"] = base64.b64encode(con).decode()

        latest_date = None
        for attachment_info in entity["mesoorExtraAttachments"]:
            if attachment_info["type"] == "candidate":
                date_added = attachment_info["dateAdded"]
                if date_added is not None:
                    # 解析日期字符串为datetime对象
                    date_added = datetime.strptime(date_added, "%Y-%m-%d %H:%M:%S")
                    if latest_date is None or date_added > latest_date:
                        latest_date = date_added
                        latest_dict = attachment_info
                        entity["mesoorExtraLatestResume"] = latest_dict


