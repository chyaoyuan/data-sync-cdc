class CGLConfig:
    gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    tip_config = {
        "tenantAlias": "bklj6280h0y7x"
    }
    base_sync_config_GqlFilter = {
        "syncModel": "GqlFilter",
        "syncAttachment": True,
    }
    entity_user = {
        "entityName": "user",
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_user_to_SystemEmployee",
             "tipEntityName": "SystemEmployee",
             "storageToTipService": "prod-ruleengine"}
        ],
    }
    # 发票
    entity_invoice = {
        "entityName": "invoice",
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
        "extraFieldNameList": "citys",
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_joborder_to_Job",
             "tipEntityName": "Job",
             "storageToTipService": "prod-ruleengine"}
        ]
    }
    # 客户
    entity_client = {
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
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_candidate_to_Resume",
             "tipEntityName": "Resume",
             "storageToTipService": "prod-ruleengine"}
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
