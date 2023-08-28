import os


class TransmitterSettings:
    transmitterHost: str = os.getenv("TRANSMITTER_HOST", "http://ruleengine.nadileaf.com")
    transmitterUrl: str = transmitterHost + "/v2/entity/{tenantAlias}/{entityType}/{openId}"