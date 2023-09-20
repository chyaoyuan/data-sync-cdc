from gllueEntityPushServer.model import EntityExtractConfig


class EntityExtractSettings:
    entity_extra_conf: EntityExtractConfig(
        **{
            "entityName": "jobOrder",
            "fieldCConfig": [
                {"fieldJMESPath": "",}
            ]
        }
    )