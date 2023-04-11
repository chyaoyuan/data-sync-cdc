import os


class Settings:
    email_decode_server_host: str = os.getenv("email_decode_server_host", "localhost")