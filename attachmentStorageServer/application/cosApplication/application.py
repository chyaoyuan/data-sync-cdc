from typing import Type

from qcloud_cos import CosS3Client

from attachmentStorageServer.settings.settings import Settings


class COSApplication:
    def __init__(self, cos_settings: Type[Settings.COSSettings]):
        self.cos_settings = cos_settings
        self.client = CosS3Client(cos_settings.config)
        # 如果权限不对会甩错，用来认证配置
        self.client.bucket_exists(cos_settings.Bucket)

    # 直接覆盖
    def put_attachment_by_path(self, local_file_path: str, key: str, header: dict):
        assert "ContentDisposition" in header
        response = self.client.upload_file(
            Bucket=self.cos_settings.Bucket,
            LocalFilePath=local_file_path,
            Key=key,
            **header
        )
        print(response)

    def get_attachment_by_key(self, key: str):
        response = self.client.get_object(
            Bucket=self.cos_settings.Bucket,
            Key=key,
        )
        print(response)
        fp = response['Body'].get_raw_stream()

        return fp.read(2)





