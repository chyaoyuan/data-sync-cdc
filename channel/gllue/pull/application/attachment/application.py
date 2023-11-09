import base64
from cgi import parse_header
from typing import Optional, Literal, List, Union
from urllib.parse import unquote, urlencode
from datetime import datetime

from loguru import logger
from tempfile import TemporaryFile
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
        for _id, attachment in zip(attachments_ids.split(","), entity["mesoorExtraAttachments"]):
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

            file = TemporaryFile()
            file.write(con)
            _, params = parse_header(headers.get("Content-Disposition"))
            filename = unquote(params.get('filename'))
            attachment["fileName"] = filename
            attachment["fileContent"] = file
            file.seek(0)
        return attachments_ids.split(',')


