import json

import requests
with open("project_info_list.jsonl", "w+") as f:
    offset = 10
    while True:
        url = f"https://www.linkedin.com/talent/api/graphql?variables=(query:(sourcingChannelTypes:List(),hiringProjectStates:List(ACTIVE,CLOSED),hiringProjectTypes:List(ATS,CAMPAIGN,JOB_POSTING,RECRUITER)),facets:List((facetType:OWNER,values:List(urn%3Ali%3Ats_seat%3A139543193),maximumNumberOfValues:100),(facetType:GEO_LOCATIONS,maximumNumberOfValues:100),(facetType:STATE,maximumNumberOfValues:100),(facetType:JOB_POSTING_STATE,maximumNumberOfValues:100),(facetType:JOB_POSTING_SOURCE_TYPE,maximumNumberOfValues:100)),sortBy:(sortByType:FAVORITE,sortOrder:DESCENDING,secondarySortByType:LAST_ENGAGED_TIME,secondarySortOrder:DESCENDING),start:{offset})&queryId=talentHiringProjects.e2c34a76dd543148733dc3d52c383cab"
        headers = {
            'authority': 'www.linkedin.com',
            'accept': 'application/vnd.linkedin.normalized+json+2.1',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'bcookie="v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3"; bscookie="v=1&20230625131234c1ec8eca-ffde-440f-8995-f02159c714c0AQGY-egn1l-MvsO24lLgd6XuCc57BNDW"; lang=v=2&lang=zh-cn; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19534%7CvVersion%7C5.1.1; _gcl_au=1.1.60394227.1687700073; li_at=AQEDAQfs8hUAeo8kAAABiPLVdbAAAAGJFuH5sFYAFHxwmGLnLkCTRuwXHM18-USa72YHSQ76NsCIENcKweJzPqwRUtWdIx8iDE_g-3eTBlaJzGnX0V3bxSK1XbaudWBe4VuFQdohMVlZGV2Mqu6WWZi8; liap=true; JSESSIONID="ajax:8187577550675074642"; li_a=AQJ2PTEmY2FwX3NlYXQ9MTM5NTQzMTkzJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTGOduw-vgZXLHTN1eTVyNG00jjSpg; cap_session_id=4355459411:1; li_er=v=1&r=urn:li:contract:207833291&t=1685998288304&g=MDIx6GM5iIj+Le1ifRGiwh7FdRUIB7b97ep1EHGhLFe1t2M=; u_tz=GMT+0800; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; li_sugr=5712ddf1-2e1a-41bb-8603-e4f30e555ec0; UserMatchHistory=AQI5Sknq5g29pwAAAYj_tz9AL_iibn2SzRLByachEQbNgzgxNa_FxX6Z31SlCeKjcMCH8GqKb6KuRA; AnalyticsSyncHistory=AQIHfSg8e1UO_wAAAYj_tz9Ar395uUZUGOtwwvomMhMR-Pr_PfQAngl2fiw10sVICkBgufsZPnTKIq02wLBIBg; lms_ads=AQFdTitMfGi7_AAAAYj_t0DacdX6cacEqtsfk2oNPOE5eeN0Ma_-fyaUfUS_snbPZ70fRHCvZWSU7Hki0UXJ8uOA6UXRa0Mv; lms_analytics=AQFdTitMfGi7_AAAAYj_t0DacdX6cacEqtsfk2oNPOE5eeN0Ma_-fyaUfUS_snbPZ70fRHCvZWSU7Hki0UXJ8uOA6UXRa0Mv; lidc="b=OB81:s=O:r=O:a=O:p=O:g=2865:u=294:x=1:i=1687919122:t=1688001722:v=2:sig=AQG5l-BJvpj0cir2JyAbUIwOfSQ38IDi"; bcookie="v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3"; lidc="b=OB81:s=O:r=O:a=O:p=O:g=2865:u=294:x=1:i=1687937850:t=1688001722:v=2:sig=AQFIrY_SdEHFJhCgsyUxccFCiNyGn82C"',
            'csrf-token': 'ajax:8187577550675074642',
            'referer': 'https://www.linkedin.com/talent/projects?filters=%7B%22OWNER%22%3A%5B%5D%2C%22STATE%22%3A%5B%22ACTIVE%22%2C%22CLOSED%22%5D%2C%22LOCATION%22%3A%5B%5D%2C%22GEO_LOCATIONS%22%3A%5B%5D%2C%22JOB_POSTING_CHANNEL_STATE%22%3A%5B%5D%2C%22JOB_POSTING_STATE%22%3A%5B%5D%2C%22JOB_POSTING_SOURCE_TYPE%22%3A%5B%5D%2C%22JOB_POSTING_PROMOTION_METHOD%22%3A%5B%5D%2C%22TYPE%22%3A%5B%22RECRUITER%22%2C%22JOB_POSTING%22%2C%22ATS%22%2C%22CAMPAIGN%22%5D%2C%22APPROVAL_STATUS%22%3A%5B%5D%2C%22APPROVAL_STATE%22%3A%5B%5D%2C%22HIRING_CONTEXTS%22%3A%5B%5D%7D&scFilters=%5B%5D&sortBy=LAST_ENGAGED&start=10',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-li-lang': 'zh_CN',
            'x-li-page-instance': 'urn:li:page:d_talent_projects_list;z7qZj7CcQw66XQTEPXdXJw==',
            'x-li-pem-metadata': 'Hiring Platform - Projects List=projects-list-view',
            'x-li-track': '{"clientVersion":"1.5.3115","mpVersion":"1.5.3115","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","mpName":"talent-solutions-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
            'x-restli-protocol-version': '2.0.0'
        }

        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            print(f"11111->{offset}")

            break
        f.write(json.dumps(response.json(), ensure_ascii=False))

        print(f"success->{offset}")
        offset = offset + 10


