from attachmentStorageServer.application.cosApplication.application import COSApplication
from attachmentStorageServer.settings.settings import Settings
c = COSApplication(Settings.COSSettings)
header = {
    "ContentDisposition": 'attachment; filename="example.txt"'

}
c.put_attachment_by_path("/Users/chenjiabin/Project/data-sync-cdc/attachmentStorageServer/application/cosApplication/example/img.png", key="11111",header=header)




i = c.get_attachment_by_key(key="11111")