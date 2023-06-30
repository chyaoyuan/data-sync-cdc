# -*- coding=utf-8
from qcloud_cos import CosConfig
import sys
import os
import logging


class COSSettings:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    secret_id = "AKIDgDXdXDgtsdASWLvHPHvLWSAdrrc9RVlm"
    secret_key = "rUt3yf7MN9hLkuqXzCBvQghTVIq9E6kB"
    region = "ap-shanghai"
    token = None
    scheme = 'https'
    Bucket = 'data-sync-storage-1314300569'

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
