import asyncio
from channel.gllue.executor.base.application import GleExeApp
id_list = [i for i in range(3441827,3441927)]
if __name__ == '__main__':
    _gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    base_sync_config = {
        "syncModel": "IdRecent",
        "syncAttachment": False,
        "orderBy": "id",
    }
    _sync_config = {
        "syncModel": "IdRecent",
        "primaryEntityName": "jobsubmission".lower(),
        "onlyFields":"operation,mark,candidate__attachment_count,candidate__joborder,candidate__note_count,candidate__englishName,candidate__chineseName,candidate__islimited,candidate__js_is_locked,candidate__locked_joborder____name__,candidate__js_lock_user____name__,candidate__js_lock_time,candidate__type,candidate__jobsubmission_count_withaccess,glluemeuser_info,is_read,portalresume_created_new_candidate,channel__code,candidate__jobsubmission_lock_type,candidate__dupalert_info,candidate__is_hide,candidate__hide_level,candidate__hider____name__,candidate__hide_time,candidate__same_name_candidate_info,candidate__contractInfo,candidate__name,candidate__company__type,candidate__company__is_parent,candidate__company__parent,candidate__company__parent__id,candidate__company__parent__type,candidate__company,candidate__title,joborder__client__name,joborder__client__candidate_authorization_remind,joborder__islimited,joborder__jobTitle,glluemeuser_info,glluemeuser__type,portalapply__portalposition__record_type,candidate__id,candidate__chineseName,candidate__islimited,joborder__id,detail,lastUpdateDate,candidate__chineseName,candidate__islimited,candidate__id,presenttoconsultant_set__date,cvsent_set__feedback__dateAdded,presenttoconsultant_set__feedback__addedBy____name__,presenttoconsultant_set__feedback__addedBy,presenttoconsultant_set__feedback__dateAdded,id,mark",
        "IdRecent": "3441827-3441927",
        "tipEntityName": "BusinessPartner",
        "storageModel": "Local",
        "gql": "lastUpdateDate__this_week&type__ns=generated",
        "storagePath": "./data",
        "convertId": "cgltest:gllue:gllue_client_contract_to_Contract",

    }
    tip_config = {
        "tenantAlias": "bklj6280h0y7x"
    }
    g = GleExeApp(_gle_user_config, base_sync_config, _sync_config, tip_config)
    asyncio.run(g.sync())
