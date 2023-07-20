from pydantic import BaseModel

# /v6/entity/{tenant}/{entity_type}/{source_id}


class PutSourceModel(BaseModel):
    tenant: str
    source_entity_type: str
    source_id: str
    payload: dict


class GetSourceModel(BaseModel):
    tenant: str
    source_entity_type: str
    source_id: str
