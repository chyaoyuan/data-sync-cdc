import os

import requests

file_name_list = os.listdir("/Users/chenjiabin/Downloads/data")
print(len(file_name_list))
for index, file_name in enumerate(file_name_list):
    url = "https://tip.mesoor.com/api/external/space/v2/candidates/upload"
    url = "https://tip.mesoor.com/api/mesoor-space/v2/candidates/upload"
    if index <= 3438:
        continue
    payload = {}
    files = [
        ('file', (f'{file_name}', open(f"/Users/chenjiabin/Downloads/data/{file_name}", 'rb'),
                  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'))
    ]
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTrpmYjlrrbmu6giLCJ0ZW5hbnRJZCI6ODAxNSwiaXNzIjoiZGVmYXVsdCIsInRlbmFudEFsaWFzIjoiYnl4MDgwMTVxM2tqbiIsImV4cCI6MTY4OTMxOTEzMzE2NSwidXNlcklkIjoiZTgyN2YxNDktYzg5My00Y2Y4LWFhZGEtMjJiMGFiOWM4OWY5IiwicHJvamVjdElkIjoiZGVmYXVsdCIsImlhdCI6MTY4ODEwOTUzMzE2NX0.P7iLjiP6zvddPkW4Hp17zyDEYAh9FcZJmXOzM0JBZXY'
    }
    res = requests.request("POST", url, headers=headers, data=payload, files=files)
    if res.status_code != 200:
        print(f"{index}==={res.content}==={res.status_code}")
    print(index)