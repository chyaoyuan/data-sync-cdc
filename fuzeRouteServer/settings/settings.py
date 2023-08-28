import os
from fuzeRouteServer.settings.transmitterSettings import TransmitterSettings


class Settings:
    TransmitterSettings = TransmitterSettings
    endPoint: list = ["GllueEntityPush"]
    ConfigMap = [
        {
            "tenantAlias": "default",
            "endPoint": "GllueEntityPush",
            "convertConfig": [
                {"entityType": "jobOrder", "convertId": ""},
                {"entityType": "jobSubMission", "convertId": ""},
                {"entityType": "candidate", "convertId": ""},
            ]
        }
    ]
