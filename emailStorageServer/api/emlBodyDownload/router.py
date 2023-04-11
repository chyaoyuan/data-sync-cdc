from fastapi import APIRouter
import base64
import uuid
from typing import Optional
import aiofiles
from starlette.responses import FileResponse
from emailStorageServer.database.executor.emlBodyStorage.application import DataBaseIntegrate as EmlBodyIntegrate
from emailStorageServer.database.executor.emlInfoStorage.application import DataBaseIntegrate as EmlInfoIntegrate

eml_download_app = APIRouter()


@eml_download_app.get(path="/email-application-server/download-email{emailUniqueId}", description="下载邮件，要求文件格式.eml", tags=["外部接口"])
async def download_eml(emailUniqueId: str):
    line_list: Optional[dict] = await EmlBodyIntegrate.GetEmailBody({"emailUniqueId": emailUniqueId})
    email_info: Optional[dict] = await EmlInfoIntegrate.GetEmailInfoByUID({"emailUniqueId": emailUniqueId})
    file_name = email_info.get("subject")
    body_list: list = [base64.b64decode(line.encode(encoding='UTF-8')) for line in line_list]
    body: bytes = b'\r\n'.join(body_list)
    unique_id = uuid.uuid4().hex
    async with aiofiles.open(f"./cache/{unique_id}.eml", mode='wb') as f:
        await f.write(body)
    return FileResponse(filename=file_name + ".eml", path=f"./cache/{unique_id}.eml")