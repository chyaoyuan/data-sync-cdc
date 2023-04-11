import requests
_json = {"connector": {"name": "test", "config": {"protocol": "IMAP", "domain": "outlook.office365.com", "email": "tangkaifeng1990@outlook.com", "password": "@TANGkaifeng@", "port": 993, "conProtocol": "SSL", "startTime": "1970-01-01T00:00:01+00:00", "autoTime": None, "autoCMD": True, "onlyUnseen": False, "seedSignal": False, "subject": None, "sender": None, "endTime": None, "lineAttachmentIgnore": False}}}
url = "http://localhost:8091/v1/emailApplication/verity/emailServerConnection"
res = requests.post(url=url,json=_json)
print(res.text)