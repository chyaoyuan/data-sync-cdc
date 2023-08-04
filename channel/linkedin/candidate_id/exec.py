import json

from loguru import logger

from channel.linkedin.获取候选人详情.get_candidate_info import get_candidate_info

with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_1.json","r") as f:
    full_candidate_list = json.loads(f.read())

    logger.info(f"去重后的任务简历人员为{len(set(full_candidate_list))}")
success_id_list = []
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate_id.jsonl", "r") as f:
    while _id := f.readline():
        _id = json.loads(_id)
        success_id_list.append(_id["id"])
    logger.info(f"去重后的已完成简历人员为{len(set(success_id_list))}")

run_list = list(set(full_candidate_list)-set(success_id_list))
logger.info(f"剩余{len(run_list)}")
headers = {
          'authority': 'www.linkedin.com',
          'accept': 'application/json',
          'accept-language': 'zh-CN,zh;q=0.9',
          'content-type': 'application/x-www-form-urlencoded',
          'cookie': 'bcookie="v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3"; bscookie="v=1&20230625131234c1ec8eca-ffde-440f-8995-f02159c714c0AQGY-egn1l-MvsO24lLgd6XuCc57BNDW"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19534%7CvVersion%7C5.1.1; _gcl_au=1.1.60394227.1687700073; liap=true; JSESSIONID="ajax:8187577550675074642"; li_a=AQJ2PTEmY2FwX3NlYXQ9MTM5NTQzMTkzJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTGOduw-vgZXLHTN1eTVyNG00jjSpg; cap_session_id=4355459411:1; li_er=v=1&r=urn:li:contract:207833291&t=1685998288304&g=MDIx6GM5iIj+Le1ifRGiwh7FdRUIB7b97ep1EHGhLFe1t2M=; u_tz=GMT+0800; li_sugr=5712ddf1-2e1a-41bb-8603-e4f30e555ec0; timezone=Asia/Shanghai; li_theme=light; li_theme_set=app; _guid=fc3c4854-ad38-4420-b0dd-1bbe435829a9; UserMatchHistory=AQJbtonmgs7oowAAAYlD_gQJlujyyARu9yzulQVWOYICRX6kvqDOCMfieqJKH6YafxATvmBYyxab7Vxh_m6DiWq7c91CxCGb34xZQ8Wf-Dp4OfAWMeeo200QXcFTZ3Yo7JW6_R_tr2UxyPIQKxGwLT9xKjBMdUNLEVwT-3Q2ZjY6jfr4Gmem9X1uSHmQAxyFUfrjvr2QIis4fhNpf3LzZdh7enS0XjITml-Hk1515p4U4N7t8XdT1CaUavlqvCuKCdlJR8Ehk0dOA8aMKiTwjDxEwqdtUienqoW04VFEKlJMyzo-_nkmf60BhGgGGA-GM5Ue5z0QFAiQ0j3Lg870cpECfmgs-84; AnalyticsSyncHistory=AQI9Eux7GDhv8AAAAYlD_gQJf3k4gFChNeGTK1txbXRdTBhsHTY3zTlMXfy1bHLhYG5fXX_cNY0Kjhf3uTIEQA; lms_ads=AQEZ-uIqDo4HSgAAAYlD_gUR8SJ5Rb13Z7jItJoRpZ_ilBY2-zT0nKTIJXpErnvzKXyj5nQfj9k1iUdNzCYGToQZU_LRTnx6; lms_analytics=AQEZ-uIqDo4HSgAAAYlD_gUR8SJ5Rb13Z7jItJoRpZ_ilBY2-zT0nKTIJXpErnvzKXyj5nQfj9k1iUdNzCYGToQZU_LRTnx6; lang=v=2&lang=zh-cn; lidc="b=OB81:s=O:r=O:a=O:p=O:g=2877:u=300:x=1:i=1689734513:t=1689817081:v=2:sig=AQGd5__LmXYaR8rFY88rtsrvPaw0DAom"; li_at=AQEDAQfs8hUAeo8kAAABiPLVdbAAAAGJkBMHs1YAzIEeNmzUzpSmCyFcg57R_12Gnisrtabp-jQMJvWFbx7zfp7pwO8WTVqUl4_aQOC6e2SFT_jzuZ8ayCY4KVM_anBjUjoazxUEmLCoR1oDnc_YwR6O; bcookie="v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3"',
          'csrf-token': 'ajax:8187577550675074642',
          'origin': 'https://www.linkedin.com',
          'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
          'x-http-method-override': 'GET',
          'x-li-lang': 'zh_CN',
          'x-li-page-instance': 'urn:li:page:d_talent_projectsHome;buiNTjOETNCCR+D3AL9JKA==',
          'x-li-pem-metadata': 'Hiring Platform - Pipeline=pipeline-profile-list',
          'x-li-track': '{"clientVersion":"1.5.3549","mpVersion":"1.5.3549","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","mpName":"talent-solutions-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
          'x-restli-protocol-version': '2.0.0'
        }
for index, candidate_id in enumerate(run_list):
    logger.info(index)
    get_candidate_info(candidate_id.split(":")[-1],headers)
    with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate_id.jsonl", "a") as f:
        f.write(json.dumps({"id": candidate_id}, ensure_ascii=False)+'\n')

