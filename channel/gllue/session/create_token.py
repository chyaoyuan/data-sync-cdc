import time

# from channel.gllue.session.model import GleUserConfig
import base64
from Crypto.Cipher import AES
from loguru import logger


class AESCrypto(object):
    def __init__(self, key=None, iv=None):
        if not iv:
            iv = '0' * 16
            self.ins = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

    def encrypt(self, txt):
        txt = pad_text(txt, 16)
        return base64.encodebytes(self.ins.encrypt(txt.encode()))

    def decrypt(self, txt):
        origin = self.ins.decrypt(base64.decodestring(txt))
        origin.strip()
        return origin


def pad_text(raw, b_s):
    raw += (b_s - len(raw) % b_s) * ' '
    return raw


def private_token(body: dict):
    timestamp = int(time.time() * 1000)
    crypto = AESCrypto(body["aesKey"])
    return crypto.encrypt('{},{},'.format(timestamp, body["account"])).decode()
