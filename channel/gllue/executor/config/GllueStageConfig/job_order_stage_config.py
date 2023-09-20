from typing import List, Optional

from pydantic import BaseModel, Field


class StageInfo(BaseModel):
    name: str
    children: Optional[list] = Field(default=[])


res = {
     "jobsubmission_status_kanban": [
          {
               "query": "joborder=146991&joborder__is_deleted=false",
               "id": "All Resume",
               "name": "All Resume",
               "key": "All Resume",
               "value": 1,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=pending",
                         "id": "All Resume^pending",
                         "name": "pending",
                         "key": "进展中",
                         "value": 1,
                         "parent_id": "All Resume",
                         "children": [],
                         "level": 1,
                         "label": "进展中"
                    }
               ],
               "level": 0,
               "label": "所有简历"
          },
          {
               "origin_key": "apply",
               "key": "Apply",
               "name": "Apply",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=apply&_hide_spec_id=1",
               "id": "apply",
               "value": 0,
               "parent_id": None,
               "children": [],
               "level": 0,
               "label": "Apply"
          },
          {
               "origin_key": "longlist",
               "key": "Screened",
               "name": "Screened",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=longlist&_hide_spec_id=1",
               "id": "longlist",
               "value": 1,
               "parent_id": None,
               "children": [],
               "level": 0,
               "label": "Screened"
          },
          {
               "origin_key": "n55393046507348800",
               "key": "Follow up",
               "name": "Follow up",
               "query": "joborder=146991&joborder__is_deleted=false&_hide_spec_id=1&jobsubmission_status_kanban=n55393046507348800",
               "id": "n55393046507348800",
               "value": 0,
               "parent_id": None,
               "children": [],
               "level": 0,
               "label": "Follow up"
          },
          {
               "origin_key": "n81171794998740720",
               "key": "Present to Consultant",
               "name": "Present to Consultant",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=n81171794998740720&_hide_spec_id=1",
               "id": "n81171794998740720",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=n81171794998740720^feedbacked&_hide_spec_id=1",
                         "id": "n81171794998740720^feedbacked",
                         "name": "feedbacked",
                         "key": "已反馈",
                         "parent_id": "n81171794998740720",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已反馈"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=n81171794998740720^non_feedback&_hide_spec_id=1",
                         "id": "n81171794998740720^non_feedback",
                         "name": "non_feedback",
                         "key": "未反馈",
                         "parent_id": "n81171794998740720",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "未反馈"
                    }
               ],
               "level": 0,
               "label": "Present to Consultant"
          },
          {
               "origin_key": "n2592208032445398",
               "key": "IV by Consultant",
               "name": "IV by Consultant",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=n2592208032445398&_hide_spec_id=1",
               "id": "n2592208032445398",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&_hide_spec_id=1&jobsubmission_status_kanban=n2592208032445398^feedbacked",
                         "id": "n2592208032445398^feedbacked",
                         "name": "feedbacked",
                         "key": "已反馈",
                         "parent_id": "n2592208032445398",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已反馈"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=n2592208032445398^non_feedback&_hide_spec_id=1",
                         "id": "n2592208032445398^non_feedback",
                         "name": "non_feedback",
                         "key": "未反馈",
                         "parent_id": "n2592208032445398",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "未反馈"
                    }
               ],
               "level": 0,
               "label": "IV by Consultant"
          },
          {
               "origin_key": "cvsent",
               "key": "Present to Client",
               "name": "Present to Client",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=cvsent&_hide_spec_id=1",
               "id": "cvsent",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=cvsent^feedbacked&_hide_spec_id=1",
                         "id": "cvsent^feedbacked",
                         "name": "feedbacked",
                         "key": "已反馈",
                         "parent_id": "cvsent",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已反馈"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=cvsent^non_feedback&_hide_spec_id=1",
                         "id": "cvsent^non_feedback",
                         "name": "non_feedback",
                         "key": "未反馈",
                         "parent_id": "cvsent",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "未反馈"
                    }
               ],
               "level": 0,
               "label": "Present to Client"
          },
          {
               "origin_key": "clientinterview",
               "key": "IV by Client",
               "name": "IV by Client",
               "query": "joborder=146991&joborder__is_deleted=false&_hide_spec_id=1&jobsubmission_status_kanban=clientinterview",
               "id": "clientinterview",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=clientinterview^feedbacked&_hide_spec_id=1",
                         "id": "clientinterview^feedbacked",
                         "name": "feedbacked",
                         "key": "已反馈",
                         "parent_id": "clientinterview",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已反馈"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&_hide_spec_id=1&jobsubmission_status_kanban=clientinterview^non_feedback",
                         "id": "clientinterview^non_feedback",
                         "name": "non_feedback",
                         "key": "未反馈",
                         "parent_id": "clientinterview",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "未反馈"
                    }
               ],
               "level": 0,
               "label": "IV by Client"
          },
          {
               "origin_key": "n83257391599134880",
               "key": "Shortlist",
               "name": "Shortlist",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=n83257391599134880&_hide_spec_id=1",
               "id": "n83257391599134880",
               "value": 0,
               "parent_id": None,
               "children": [],
               "level": 0,
               "label": "Shortlist"
          },
          {
               "origin_key": "offersign",
               "key": "Offer",
               "name": "Offer",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=offersign&_hide_spec_id=1",
               "id": "offersign",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&_hide_spec_id=1&jobsubmission_status_kanban=offersign^feedbacked_pass",
                         "id": "offersign^feedbacked_pass",
                         "name": "feedbacked_pass",
                         "key": "offersign^feedbacked_pass",
                         "parent_id": "offersign",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已接受"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=offersign^feedbacked_reject&_hide_spec_id=1",
                         "id": "offersign^feedbacked_reject",
                         "name": "feedbacked_reject",
                         "key": "offersign^feedbacked_reject",
                         "parent_id": "offersign",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已拒绝"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=offersign^non_feedback&_hide_spec_id=1",
                         "id": "offersign^non_feedback",
                         "name": "non_feedback",
                         "key": "未反馈",
                         "parent_id": "offersign",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "未反馈"
                    }
               ],
               "level": 0,
               "label": "Offer"
          },
          {
               "origin_key": "onboard",
               "key": "Onboard",
               "name": "Onboard",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=onboard&_hide_spec_id=1",
               "id": "onboard",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=onboard^in_probation&_hide_spec_id=1",
                         "id": "onboard^in_probation",
                         "name": "in_probation",
                         "key": "onboard^in_probation",
                         "parent_id": "onboard",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "试用期内"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=onboard^out_of_probation&_hide_spec_id=1",
                         "id": "onboard^out_of_probation",
                         "name": "out_of_probation",
                         "key": "onboard^out_of_probation",
                         "parent_id": "onboard",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已过试用期"
                    }
               ],
               "level": 0,
               "label": "Onboard"
          },
          {
               "origin_key": "invoice",
               "key": "Billing",
               "name": "Billing",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=invoice&_hide_spec_id=1",
               "id": "invoice",
               "value": 0,
               "parent_id": None,
               "children": [
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&_hide_spec_id=1&jobsubmission_status_kanban=invoice^approvaled",
                         "id": "invoice^approvaled",
                         "name": "approvaled",
                         "key": "已审批",
                         "parent_id": "invoice",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "已审批"
                    },
                    {
                         "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=invoice^no_approval&_hide_spec_id=1",
                         "id": "invoice^no_approval",
                         "name": "no_approval",
                         "key": "未审批",
                         "parent_id": "invoice",
                         "value": 0,
                         "children": [],
                         "level": 1,
                         "label": "未审批"
                    }
               ],
               "level": 0,
               "label": "Billing"
          },
          {
               "origin_key": "reject",
               "key": "Reject",
               "name": "Reject",
               "query": "joborder=146991&joborder__is_deleted=false&jobsubmission_status_kanban=reject&_hide_spec_id=1",
               "id": "reject",
               "value": 0,
               "parent_id": None,
               "children": [],
               "level": 0,
               "label": "Reject"
          }
     ]
}
remap_job_submission_status: list = []

def init_job_submission_status_filed(status_list, field_list, lv_name: Optional[str] = ""):
    for status in status_list:
        stage_info = StageInfo(**status)
        if lv_name and not stage_info.children:
            lv_name = f"{lv_name}-{stage_info.name}"
            remap_job_submission_status.append(lv_name)
        elif not stage_info.children:
            lv_name = stage_info.name
            remap_job_submission_status.append(stage_info.name)
        if children := stage_info.children:
            init_job_submission_status_filed(children, field_list, lv_name)


init_job_submission_status_filed(res["jobsubmission_status_kanban"], remap_job_submission_status)
print(remap_job_submission_status)


