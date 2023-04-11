# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
from loguru import logger
from sqlalchemy_utils import database_exists, create_database
from starlette.middleware.cors import CORSMiddleware

from emailStorageServer.config import Settings
from emailStorageServer.api.routers import router_list
from emailStorageServer.database.executor.application import application as database_app

app = FastAPI(title="邮件增删改查服务", description="增改查邮件")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

for router in router_list:
    app.include_router(router)


@app.on_event("startup")
async def startup():
    await database_app.settings.DatabaseSettings.db_instance.connect()
    database_app.init_tables()


if __name__ == '__main__':
    uvicorn.run("server:app", host="0.0.0.0", port=8095, reload=True)
