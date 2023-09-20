import uvicorn
from utils.logger import logger
from fastapi import FastAPI
from entityStorageServer.database.executor.application import database_app
from fastapi.responses import JSONResponse


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database_app.settings.DatabaseSettings.db_instance.connect()
    database_app.init_tables()


@app.put("/v6/entity/{tenant}/{entity_type}/{source_id}")
async def put_entity(tenant: str, entity_type: str, source_id: str, payload: dict):
    body = {
        "tenant": tenant,
        "entity_type": entity_type,
        "source_id": source_id,
        "payload": payload
    }
    await database_app.entity_info.put_entity(body)


@app.get("/v6/entity/{tenant}/{entity_type}/{source_id}")
async def get_entity(tenant: str, entity_type: str, source_id: str):
    body = {
        "tenant": tenant,
        "entity_type": entity_type,
        "source_id": source_id,
    }
    entity = await database_app.entity_info.get_entity(body)
    if entity:
        return JSONResponse(content=entity["payload"], status_code=200)
    return JSONResponse(content={}, status_code=404)


@app.post("/v6/connection/{tenant}/connection")
async def put_entity(tenant: str, entity_type: str, source_id: str, payload: dict):
    body = {
        "tenant": tenant,
        "entity_type": entity_type,
        "source_id": source_id,
        "payload": payload
    }
    await database_app.entity_info.put_entity(body)


@app.post("/v6/connection/{tenant}/connection")
async def put_entity(tenant: str, entity_type: str, source_id: str, payload: dict):
    body = {
        "tenant": tenant,
        "source_entity_type": entity_type,
        "source_open_id": source_id,
        "entity_type": entity_type,
        "source_id": source_id,
    }
    await database_app.entity_info.put_entity(body)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9400)