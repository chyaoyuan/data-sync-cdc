# -*- coding: utf-8 -*-
import base64
import uuid
from typing import List, Optional
from fastapi import UploadFile, File, APIRouter
from loguru import logger

from emailStorageServer.api.emlBodyUpload.model import OverWriteModel
from emailStorageServer.config import Settings
from emailStorageServer.data_model import UpLoadEmlFilesResponse, ResponseEmailDecodeModel, Source
from utils.custom_aiohttp_session import session, callback
from emailStorageServer.database.executor.application import application as database_app
eml_upload_app = APIRouter()


@eml_upload_app.post(path="/email-application-server/upload-email", description="上传邮件，要求文件格式.eml", tags=["外部接口"],response_model=UpLoadEmlFilesResponse)
async def upload_email(tenant: str, overwrite: Optional[OverWriteModel], files: List[UploadFile] = File(...)):
    for file in files:
        if file.content_type != "message/rfc822" or not file.filename.endswith(".eml"):
            return {"code": 403, "msg": "上传的邮件格式必须为.eml"}
    for file in files:
        file_byte: bytes = await file.read()
        eml_body_b64 = [base64.b64encode(line.encode()).decode() for line in file_byte.decode().split("\r\n")]
        logger.info(file.filename)
        body = {
            "index": "000000000000",
            "emailBodyB64": eml_body_b64,
            "RequestUID": uuid.uuid4().hex,
            "tenant": tenant,
            "lineAttachmentIgnore": True,
            "forwardHeaderReplace": True
        }
        status, context = await session.post(Settings.eml_decode_url, json=body, func=callback)
        eml_info = ResponseEmailDecodeModel(**context)
        eml_info_dict = ResponseEmailDecodeModel(**context).dict()
        eml_info_dict["id"] = eml_info.emailUniqueId
        eml_info_dict["source"] = Source.customer
        eml_info_dict["fileName"] = file.filename
        eml_info_dict["tenant"] = tenant
        eml_info_dict["body"] = eml_body_b64
        for k, v in overwrite.Config.dict().items():
            if v:
                eml_info_dict[k] = v

        await database_app.email_body_app.upsert_email_body(eml_info_dict)
        await database_app.email_info_app.upsert_email_info(eml_info_dict)


        # if status == 200:
        #     eml_info = ResponseEmailDecodeModel(**context)
        #     eml_stg_info: Optional[EmailStatusModel] = await EmlInfoIntegrate.GetEmailInfoByUID({"emailUniqueId": eml_info.emailUniqueId})
        #     if eml_stg_info:
        #         info.insert_exist(EmailInfoSketchModel(**eml_info.dict()))
        #         logger.info(f"客户上传 邮件已存在 id->{eml_info.emailUniqueId} time->{eml_info.receiveTime} subject->{eml_info.subject}")
        #     else:
        #         eml_info_d: dict = eml_info.dict()
        #         eml_info_d["id"] = eml_info_d["emailUniqueId"]
        #         eml_info_d["tenant"] = tenant
        #         eml_info_d["source"] = Source.customer
        #         eml_info_d["body"] = eml_body_b64
        #         await EmlBodyIntegrate.UpsertEmail(eml_info_d)
        #         await EmlInfoIntegrate.UpsertEmail(eml_info_d)
        #         info.insert_insert(EmailInfoSketchModel(**eml_info.dict()))
        #         logger.info(f"客户上传 邮件已上传 id->{eml_info.emailUniqueId} time->{eml_info.receiveTime} subject->{eml_info.subject}")
        # else:
        #     return JSONResponse(status_code=status, content={"mas": f"{context}", "result": None})
        # return JSONResponse(status_code=fast_api_status.HTTP_200_OK, content={"result": info.result()})
        # position: Optional[str] = Field(..., description="职位名称")
