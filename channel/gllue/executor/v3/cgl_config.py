from channel.gllue.executor.model import SyncModel


class CGLConfig:
    SyncModel = SyncModel
    gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    tip_config_prod = {
        "tenantAlias": "shanghaidezhuqiyeguanli-188"
    }
    tip_config_dev = {
        "tenantAlias": "cgltest"
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
        "syncAttachment": True,
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
        "syncAttachment": True,
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_candidate_to_Resume",
             "tipEntityName": "Resume",
             "storageToTipService": "prod-ruleengine",},
            {"convertId": "cgltest:gllue:gllue_note_to_Note",
             "jmeSPath": "standardFields.entity",
             "tipEntityName": "Resume",
             "storageToTipService": "prod-mesoor-space"}
        ]
    }

    entity_candidate_old = {
        "entityName": "candidate",
        "extraFieldNameList": "citys",
        "fieldList": ["note"],
        "syncAttachment": False,
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_candidate_to_Resume",
             "tipEntityName": "Resume",
             "storageToTipService": "prod-ruleengine", }
        ]
    }
    entity_contract = {
        "entityName": "clientcontract",
        "syncAttachment": False,
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_client_contract_to_Contract",
             "tipEntityName": "Contract",
             "storageToTipService": "prod-ruleengine"}
        ]
    }
    # 流程阶段
    entity_jobsubmission = {
        "entityName": "jobsubmission",
        "storageToTipConfig": [
            {"convertId": "cgltest:gllue:gllue_jobsubmission_to_HydrogenTask",
             "tipEntityName": "HydrogenTask",
             "storageToTipService": "prod-ruleengine"}
        ],

        "onlyFields": "follow_up_set__date,longlist_set__lastUpdateDate,longlist_set__dateAdded,shortlist_set__dateAdded,presenttoconsultant_set__dateAdded,operation,candidate__joborder,candidate__englishName,candidate__chineseName,candidate__islimited,candidate__js_is_locked,candidate__locked_joborder____name__,candidate__js_lock_user____name__,candidate__js_lock_time,candidate__type,candidate__jobsubmission_count_withaccess,glluemeuser_info,is_read,portalresume_created_new_candidate,channel__code,candidate__jobsubmission_lock_type,candidate__dupalert_info,candidate__is_hide,candidate__hide_level,candidate__hider____name__,candidate__hide_time,candidate__same_name_candidate_info,candidate__contractInfo,candidate__name,candidate__company__type,candidate__company__is_parent,candidate__company__parent,candidate__company__parent__id,candidate__company__parent__type,candidate__company,candidate__title,joborder__client__name,joborder__client__candidate_authorization_remind,joborder__islimited,joborder__jobTitle,glluemeuser_info,glluemeuser__type,portalapply__portalposition__record_type,candidate__id,candidate__chineseName,candidate__islimited,joborder__id,detail,lastUpdateDate,candidate__addedBy____name__,candidate__addedBy,candidate__owner____name__,candidate__owner,cvsent_set__user____name__,cvsent_set__user,longlist_set__addedBy____name__,longlist_set__addedBy,id,joborder__id,candidate__chineseName,candidate__islimited,candidate__id,candidate__candidateexperience_set__client__type,candidate__candidateexperience_set__client__is_parent,candidate__candidateexperience_set__client__parent,candidate__candidateexperience_set__client__parent__id,candidate__candidateexperience_set__client__parent__type,candidate__candidateexperience_set__client,joborder__client__name,joborder__client__type,joborder__client____name__,joborder__client__is_parent,joborder__client__parent,joborder__client__parent__id,joborder__client__parent__type,joborder__client,user____name__,user,apply_time,dateAdded,presenttoconsultant_set__user____name__,presenttoconsultant_set__user,joborder__id,user__isleader,user__team____name__,user__team,joborder____name__,joborder,candidate__gllueextClient_report_comments,candidate__candidateexperience_set__title,candidate__candidateexperience_set__end,candidate__expected_salary,estimate_onboardDate,candidate__channel____name__,candidate__channel__hunter,candidate__channel,candidate__candidateeducation_set__school_type,candidate__candidateeducation_set__school_aid,candidate__candidateeducation_set__school,candidate__candidateeducation_set__degree,candidate__candidateeducation_set__start,candidate__candidateeducation_set__end,joborder__client__industry__id,shortlist_set__gllueext_shortliststatus,candidate__candidateeducation_set__candidateeducation_set__degree,candidate__candidateeducation_set__highest_degree,candidate__candidateeducation_set__secondary_degree,candidate__candidateeducation_set__first_degree,candidate__candidateeducation_set,candidate__candidateeducation_set__major,candidate__candidateexperience_set,candidate__type,candidate__company__is_parent,candidate__company__parent__id,candidate__company__parent__type,candidate__company__contractInfo,candidate__company__candidate_authorization_remind,candidate__company__type,candidate__company__name,clientinterview_round,clientinterview_set__type,clientinterview_set,candidate__tags,cvsent_set__date,clientinterview_set__dateAdded,clientinterview_set__date,presenttoconsultant_set__date,cvsent_set__feedback__dateAdded,presenttoconsultant_set__feedback__addedBy____name__,presenttoconsultant_set__feedback__addedBy,presenttoconsultant_set__feedback__dateAdded,rating_score,cvsent_set__dateAdded,joborder__openDate,presenttoconsultant_set__addedBy____name__,presenttoconsultant_set__addedBy,follow_up_set__dateAdded,candidate__latest_action,joborder__joborderuser_set__user____name__,joborder__joborderuser_set__type,joborder__joborderuser_set,presenttoconsultant_set__gllueext_fk_1626747538537____name__,presenttoconsultant_set__gllueext_fk_1626747538537,candidate__lastContactBy____name__,candidate__lastContactBy,candidate__company__id,joborder__dateAdded,candidate__gender,candidate____name__,candidate__locations,candidate____name__,candidate__citys,candidate__dateOfBirth,candidate__yearNull,candidate__monthNull,candidate__dayNull,candidate__age,mark"
    }
