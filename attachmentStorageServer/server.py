from fastapi import FastAPI, File, UploadFile

from attachmentStorageServer.application.cosApplication.application import COSApplication
from attachmentStorageServer.settings.settings import Settings

app = FastAPI()

cos = COSApplication(Settings.COSSettings)


@app.put("/v6/entity/{tenant}/{entity_type}/{source_id}")
# 上传文件的接口
@app.post("/v6/entity/{tenant}/{entity_type}/{source_id}")
def upload_file(file: UploadFile):

    # 检查上传的文件类型
    allowed_file_extensions = ["jpg", "jpeg", "png", "gif"]
    file_extension = file.filename.split(".")[-1]
    if file_extension not in allowed_file_extensions:
        return {"error": "Invalid file extension"}

    # 保存上传的文件到服务器
    with open(f"uploads/{file.filename}", "wb") as file_object:
        file_object.write(file.file.read())
    cos.put_attachment_by_path()
    return {"filename": file.filename}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)