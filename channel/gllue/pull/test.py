import time
import base64


# def pad_text(raw, BS):
#     raw += (BS - len(raw) % BS) * ' '
#     return raw
#
#
# class AESCrypto(object):
#     def __init__(self, key=None, iv=None):
#         from Crypto.Cipher import AES
#         if not iv:
#             iv = '0' * 16
#         self.ins = AES.new(key, AES.MODE_CBC, iv)
#
#     def encrypt(self, txt):
#         txt = pad_text(txt, 16)
#         return base64.encodestring(self.ins.encrypt(txt))
#
#     def decrypt(self, txt):
#         origin = self.ins.decrypt(base64.decodestring(txt))
#         origin.strip()
#         return origin
#
from urllib.parse import quote

from loguru import logger
aes_key = '824531e8cad2a287'


def get_timestamp_string():
    timestamp = str(int(time.time() * 1000))
    logger.info(len(str(timestamp)))
    return timestamp


def get_email_string():
    email = 'api@fsg.com.cn'
    return email


def run():
    body = get_timestamp_string() + ',' + get_email_string() + ","
    while len(body) % 16 != 0:
        body = body + " "
    return body
from Crypto.Cipher import AES



if __name__ == '__main__':
    i = run()
    logger.info(i)
    logger.info(len(i))

    # password = b'eqs214hvIHEY7Reg'  # 秘钥，b就是表示为bytes类型
    # text = b'1477971027294,system@gllue.com, '  # 需要加密的内容，bytes类型

    password: bytes = b'824531e8cad2a287'  # 秘钥，b就是表示为bytes类型
    text:bytes = run().encode()
    aes = AES.new(password, AES.MODE_CBC)  # 创建一个aes对象
    # AES.MODE_ECB 表示模式是ECB模式
    i = AES.new(password, AES.MODE_CBC, b'0'*16).encrypt(text)
    logger.info(quote(base64.encodebytes(i)))
# ARP%2B5XryVt0Wo47jlMFwZPUq253azoOR3WODCThFJBU%3D%0A
# ARP%2B5XryVt0Wo47jlMFwZPUq253azoOR3WODCThFJBU%3D





# private_token = AESCrypto(aes_key).encrypt('{},{},'.format(timestamp, email))