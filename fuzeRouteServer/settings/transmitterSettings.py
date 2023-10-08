import os


class TransmitterSettings:
    # transmitterHost: str = os.getenv("TRANSMITTER_HOST", "http://ruleengine.nadileaf.com")
    transmitterHost: str = os.getenv("TRANSMITTER_HOST", "http://localhost:57978")
    transmitterUrl: str = transmitterHost + "/v2/entity/{tenantAlias}/{entityType}/{openId}"