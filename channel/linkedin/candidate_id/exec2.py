


import json

from loguru import logger

from channel.linkedin.获取候选人详情.get_candidate_info import get_candidate_info

# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_1.json","r") as f:
#     full_candidate_list = json.loads(f.read())
#     print(len(set(full_candidate_list)))
# success_id_list = []
# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate_id.jsonl", "r") as f:
#     while _id := f.readline():
#         _id = json.loads(_id)
#         success_id_list.append(_id["id"])
#     print(len(set(success_id_list)))
#
# run_list = list(set(full_candidate_list)-set(success_id_list))
# logger.info(f"剩余{len(run_list)}")
# headers = {
#   'authority': 'www.linkedin.com',
#   'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
#   'x-li-track': '{"clientVersion":"1.5.3643","mpVersion":"1.5.3643","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","mpName":"talent-solutions-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
#   'x-li-lang': 'zh_CN',
#   'sec-ch-ua-mobile': '?0',
#   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 QQBrowser/5.0.4.207',
#   'x-li-page-instance': 'urn:li:page:d_talent_projectsHome;AEQtqqtCR/W5QJKeWTiAew==',
#   'content-type': 'application/x-www-form-urlencoded',
#   'accept': 'application/json',
#   'csrf-token': 'ajax:5715864652291822049',
#
#   'x-restli-protocol-version': '2.0.0',
#   'x-http-method-override': 'GET',
#   'sec-ch-ua-platform': '"macOS"',
#   'origin': 'https://www.linkedin.com',
#   'sec-fetch-site': 'same-origin',
#   'sec-fetch-mode': 'cors',
#   'sec-fetch-dest': 'empty',
#   'referer': 'https://www.linkedin.com/talent/hire/343408354/manage/all',
#   'accept-language': 'zh-CN,zh;q=0.9',
#
# "cookie":"""lang=v=2&lang=zh-cn; bcookie="v=2&9e118c68-51bf-4f49-8dfc-b5118bf10d6b"; bscookie="v=1&20230724052431d019967c-1e66-4e86-88a6-3a5b8f2da1fdAQHm0rHvOH1flYiCpOQOk_U1HDN5E9pe"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=37427139670455947393881708517462301521; _gcl_au=1.1.931650968.1690176311; JSESSIONID="ajax:5715864652291822049"; li_cc=AQFqr2848-nJ3AAAAYmGW-rJpnSyhpUtdccya_hKgQ5JmJYqtfuBJVo-q2zzQHrLBA_27cVH3OQx; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19563%7CMCMID%7C36929228034292934963824038117011105946%7CMCAAMLH-1690781131%7C11%7CMCAAMB-1690781131%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1690183531s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1904315386; li_at=AQEDATSZ_DkEpmzGAAABiYZcNwYAAAGJqmi7BlYATolkaTJ_qi1_2YyfkAyFdXEQrTG_osomupKR2dXUN4mUlim_UA33qY6O_2epZhZ95Yg7AjTYmn3Ul4nuQrGcj_EjYW_0TY1ERSdtas6IUpWCkq0A; liap=true; lidc="b=OB09:s=O:r=O:a=O:p=O:g=4208:u=114:x=1:i=1690176338:t=1690250550:v=2:sig=AQFjb4ValcSlZ3d1NxJF1nJ2PLKMrE-L"; li_a=AQJ2PTEmY2FwX3NlYXQ9MjU3NjQwMzAxJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTEp7wzthd8FvACZNH-U-M4jOtTV_A; cap_session_id=4387499601:1; li_er=v=1&r=urn:li:contract:207833291&t=1688473370374&g=MDIx1JLKTXj78qbOt3C6lZOxykm38MKc/RyMzQBkm2/YEMw=; u_tz=GMT+08:00; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D"""}
# for index, candidate_id in enumerate(run_list):
#     logger.info(index)
#     get_candidate_info(candidate_id.split(":")[-1],headers)
#     with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate_id.jsonl", "a") as f:
#         f.write(json.dumps({"id": candidate_id}, ensure_ascii=False)+'\n')



import asyncio
import json

import aiohttp
from loguru import logger

from channel.linkedin.获取候选人详情.get_candidate_info import get_candidate_info, _asy_get_candidate_info


async def run():
    with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_3.json", "r") as f:
        full_candidate_list = json.loads(f.read())

        logger.info(f"去重后的任务简历人员为{len(set(full_candidate_list))}")
    success_id_list = []
    with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate_id.jsonl",
              "r") as f:
        while _id := f.readline():
            _id = json.loads(_id)
            success_id_list.append(_id["candidateId"])
        logger.info(f"去重后的已完成简历人员为{len(set(success_id_list))}")

    run_list = list(set(full_candidate_list) - set(success_id_list))
    logger.info(f"剩余{len(run_list)}")
    headers = {
        'authority': 'www.linkedin.com',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
        'x-li-track': '{"clientVersion":"1.5.3643","mpVersion":"1.5.3643","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","mpName":"talent-solutions-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
        'x-li-lang': 'zh_CN',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 QQBrowser/5.0.4.207',
        'x-li-page-instance': 'urn:li:page:d_talent_projectsHome;AEQtqqtCR/W5QJKeWTiAew==',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json',
        'csrf-token': 'ajax:5715864652291822049',

        'x-restli-protocol-version': '2.0.0',
        'x-http-method-override': 'GET',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://www.linkedin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.linkedin.com/talent/hire/343408354/manage/all',
        'accept-language': 'zh-CN,zh;q=0.9',

        "cookie": """lang=v=2&lang=zh-cn; bcookie="v=2&9e118c68-51bf-4f49-8dfc-b5118bf10d6b"; bscookie="v=1&20230724052431d019967c-1e66-4e86-88a6-3a5b8f2da1fdAQHm0rHvOH1flYiCpOQOk_U1HDN5E9pe"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=37427139670455947393881708517462301521; _gcl_au=1.1.931650968.1690176311; JSESSIONID="ajax:5715864652291822049"; li_cc=AQFqr2848-nJ3AAAAYmGW-rJpnSyhpUtdccya_hKgQ5JmJYqtfuBJVo-q2zzQHrLBA_27cVH3OQx; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19563%7CMCMID%7C36929228034292934963824038117011105946%7CMCAAMLH-1690781131%7C11%7CMCAAMB-1690781131%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1690183531s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1904315386; li_at=AQEDATSZ_DkEpmzGAAABiYZcNwYAAAGJqmi7BlYATolkaTJ_qi1_2YyfkAyFdXEQrTG_osomupKR2dXUN4mUlim_UA33qY6O_2epZhZ95Yg7AjTYmn3Ul4nuQrGcj_EjYW_0TY1ERSdtas6IUpWCkq0A; liap=true; lidc="b=OB09:s=O:r=O:a=O:p=O:g=4208:u=114:x=1:i=1690176338:t=1690250550:v=2:sig=AQFjb4ValcSlZ3d1NxJF1nJ2PLKMrE-L"; li_a=AQJ2PTEmY2FwX3NlYXQ9MjU3NjQwMzAxJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTEp7wzthd8FvACZNH-U-M4jOtTV_A; cap_session_id=4387499601:1; li_er=v=1&r=urn:li:contract:207833291&t=1688473370374&g=MDIx1JLKTXj78qbOt3C6lZOxykm38MKc/RyMzQBkm2/YEMw=; u_tz=GMT+08:00; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D"""}
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[
            _asy_get_candidate_info(candidate_id.split(":")[-1],headers,session,candidate_id,semaphore) for candidate_id in run_list
        ])
if __name__ == '__main__':


    asyncio.run(run())