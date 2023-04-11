import requests
import json

from connectionServer.Application.base.baseApplication import BaseApplication


class ConnectorIntegrate(BaseApplication):


    async def get_connector(self):
        payload = json.dumps({
            "name": "inventory-connector",
            "config": {
                "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
                "database.hostname": "postgres",
                "database.port": "5432",
                "database.user": "postgres",
                "database.password": "postgres",
                "database.dbname": "postgres",
                "database.server.name": "debezium",
                "slot.name": "inventory_slot",
                "table.include.list": "inventory.orders,inventory.products",
                "publication.name": "dbz_inventory_connector",
                "publication.autocreate.mode": "filtered",
                "plugin.name": "pgoutput"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
