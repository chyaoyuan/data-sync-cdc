from channel.gllue.executor.model import SyncModel


class CGLConfig:
    SyncModel = SyncModel
    gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    tip_config = {
        "tenantAlias": "cgltest"
    }
    base_sync_config_GqlFilter = {
        "syncModel": "GqlFilter",

    }
    base_sync_config_IdRecent = {
        "syncModel": "IdRecent",

    }
    entity_user = {
        "entityName": "user",
        "syncAttachment": True,
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_user_to_SystemEmployee",
             "tipEntityName": "SystemEmployee",
             "storageToTipService": "prod-ruleengine"}
        ],
    }
    # 发票
    entity_invoice = {
        "entityName": "invoice",
        "syncAttachment": True,
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_invoice_to_Invoice",
             "tipEntityName": "Invoice",
             "storageToTipService": "prod-ruleengine"}
        ],
        "extraFieldName": "jobsubmission__candidate__id",

    }
    # 项目
    entity_job_order = {
        "entityName": "joborder",
        "syncAttachment": False,
        "extraFieldNameList": "citys",
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_joborder_to_Job",
             "tipEntityName": "Job",
             "storageToTipService": "prod-ruleengine"}
        ]
    }
    # 客户
    entity_client = {
        "syncAttachment": False,
        "entityName": "client",
        "extraFieldNameList": "citys",
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_client_to_BusinessPartner",
             "tipEntityName": "BusinessPartner",
             "storageToTipService": "prod-ruleengine"}
        ]
    }
    # 人才
    entity_candidate = {
        "entityName": "candidate",
        "extraFieldNameList": "citys",
        "fieldList": ["note"],
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_candidate_to_Resume",
             "tipEntityName": "Resume",
             "storageToTipService": "prod-ruleengine",},
            {"convertId": "cgltest:gllue:gllue_note_to_Note",
             "jmeSPath":"standardFields.entity",
             "tipEntityName": "Resume",
             "storageToTipService": "prod-mesoor-space"}
        ]
    }
    entity_contract = {
        "entityName": "clientcontract",
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_client_contract_to_Contract",
             "tipEntityName": "Contract",
             "storageToTipService": "prod-ruleengine"}
        ]
    }
