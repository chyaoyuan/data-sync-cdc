import asyncio
import json
import time

import aiohttp
from loguru import logger

from channel.linkedin.applicant.applicantion import Application

with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/applicant/data/project_id_4.json") as f:
    project_id_list = json.loads(f.read())

async def run():

    _headers = {
  'authority': 'www.linkedin.com',
  'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
  'x-li-track': '{"clientVersion":"1.5.3643","mpVersion":"1.5.3643","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","mpName":"talent-solutions-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
  'x-li-lang': 'zh_CN',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 QQBrowser/5.0.4.207',
  'x-li-page-instance': 'urn:li:page:d_talent_projectsHome;AEQtqqtCR/W5QJKeWTiAew==',
  'content-type': 'application/x-www-form-urlencoded',
  'accept': 'application/json',
  'csrf-token': 'ajax:5869431920008066618',

  'x-restli-protocol-version': '2.0.0',
  'x-http-method-override': 'GET',
  'sec-ch-ua-platform': '"macOS"',
  'origin': 'https://www.linkedin.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.linkedin.com/talent/hire/343408354/manage/all',
  'accept-language': 'zh-CN,zh;q=0.9',

#"cookie":"""lang=v=2&lang=zh-cn; bcookie="v=2&9e118c68-51bf-4f49-8dfc-b5118bf10d6b"; bscookie="v=1&20230724052431d019967c-1e66-4e86-88a6-3a5b8f2da1fdAQHm0rHvOH1flYiCpOQOk_U1HDN5E9pe"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=37427139670455947393881708517462301521; _gcl_au=1.1.931650968.1690176311; JSESSIONID="ajax:5715864652291822049"; li_cc=AQFqr2848-nJ3AAAAYmGW-rJpnSyhpUtdccya_hKgQ5JmJYqtfuBJVo-q2zzQHrLBA_27cVH3OQx; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19563%7CMCMID%7C36929228034292934963824038117011105946%7CMCAAMLH-1690781131%7C11%7CMCAAMB-1690781131%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1690183531s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1904315386; li_at=AQEDATSZ_DkEpmzGAAABiYZcNwYAAAGJqmi7BlYATolkaTJ_qi1_2YyfkAyFdXEQrTG_osomupKR2dXUN4mUlim_UA33qY6O_2epZhZ95Yg7AjTYmn3Ul4nuQrGcj_EjYW_0TY1ERSdtas6IUpWCkq0A; liap=true; lidc="b=OB09:s=O:r=O:a=O:p=O:g=4208:u=114:x=1:i=1690176338:t=1690250550:v=2:sig=AQFjb4ValcSlZ3d1NxJF1nJ2PLKMrE-L"; li_a=AQJ2PTEmY2FwX3NlYXQ9MjU3NjQwMzAxJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTEp7wzthd8FvACZNH-U-M4jOtTV_A; cap_session_id=4387499601:1; li_er=v=1&r=urn:li:contract:207833291&t=1688473370374&g=MDIx1JLKTXj78qbOt3C6lZOxykm38MKc/RyMzQBkm2/YEMw=; u_tz=GMT+08:00; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D"""
# "cookie":"""bcookie="v=2&f4ce890e-348c-483d-8b6d-f92d7fc6da6d"; bscookie="v=1&20230724015432c507f5bf-91a8-41bb-8f25-ee82e1ddf291AQFAHIlmRwYBDzIGPF4DPxUPNh-Ly8eh"; lidc="b=OB68:s=O:r=O:a=O:p=O:g=4895:u=610:x=1:i=1690182102:t=1690254938:v=2:sig=AQEPPKXJGyGUueGA-hBErPukg27QjKpX"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19563%7CMCMID%7C53526586825724856920841995788241120528%7CMCAAMLH-1690768477%7C11%7CMCAAMB-1690768477%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1690170877s%7CNO…RJtnYhZ5FFBbxhGaDRaoftUOXw2FT9NFBdENpe291dKGMTGuUjBOHEKWrUNomfMpkzryRkEa2saZwjP7YwwKsyUgwklzZo; _guid=b71e630b-f7cc-4000-afb8-c7545d93c4a6; li_sugr=5de45e3f-96a4-49e0-9a5d-ea3777c2983c; AnalyticsSyncHistory=AQJg0S_t5ll3ZgAAAYmGtCDMP8js9BFGe-Y4e_Onmfk4OEo7nOOeOyGhr_oDq4SI0z27gDvPGd1vDV6bfEaVlQ; lms_ads=AQHuTA6WlDz_qAAAAYmGtCGRdHEQ5DtDiJnhmXreLuKRabtLPZmRbJGT-3K1Juq0asn4IHXhPbf-563t_bJzgFvWCAV5qyri; lms_analytics=AQHuTA6WlDz_qAAAAYmGtCGRdHEQ5DtDiJnhmXreLuKRabtLPZmRbJGT-3K1Juq0asn4IHXhPbf-563t_bJzgFvWCAV5qyri"""}
"cookie":"""bcookie="v=2&f4ce890e-348c-483d-8b6d-f92d7fc6da6d"; bscookie="v=1&20230724015432c507f5bf-91a8-41bb-8f25-ee82e1ddf291AQFAHIlmRwYBDzIGPF4DPxUPNh-Ly8eh"; lidc="b=OB68:s=O:r=O:a=O:p=O:g=4895:u=610:x=1:i=1690182102:t=1690254938:v=2:sig=AQEPPKXJGyGUueGA-hBErPukg27QjKpX"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19563%7CMCMID%7C53526586825724856920841995788241120528%7CMCAAMLH-1690768477%7C11%7CMCAAMB-1690768477%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1690170877s%7CNONE%7CvVersion%7C5.1.1; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=53703595339015966630819779969307533019; cap_session_id=4387402101:1; li_er=v=1&r=urn:li:contract:207833291&t=1688465570819&g=MDIx94zLhQ+VznxkddiK5UHR5238tYPSBktb8mo/nWDLt1Q=; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; u_tz=GMT+08:00; visit=v=1&M; lang=v=2&lang=zh-cn; JSESSIONID="ajax:5869431920008066618"; li_rm=AQFuWXVq8t6sRQAAAYmF3y7xDIB48PXRl6vo5szd96gHL7c5DLALCoAbCLAfgPV-p6YMDPQH07snnwgiAiMEAQw2FXCg7VXGeVbko9X-1pZA6aJ6j4Zyw4q1; liap=true; li_at=AQEDAROSx6QBjM4EAAABiYXlNAMAAAGJqfG4A1YALbbrlMr0LrluATHfagqWHZQHCIJYeZSmibLMH5eZUjQ11LLe08H9zWux44_KyG7v5s99SgcobST1R5lc4VayboJfJPcBT9nNcg6DYGQRZ66jaP3e; li_a=AQJ2PTEmY2FwX3NlYXQ9MTM5NTQzMjAzJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTHCl2E_SA4lBYi1CtnID8LpaZ38dw; li_cc=AQEWuSoLjsujpgAAAYmGtAZmgNaKe034uohqhsc3NPuvKEOgzfqKbMHneTohlnm5ekRx4aIl-oIO; li_ce=AQEdwAoPZlLUPgAAAYmGtAf51lRNHbUVSYAafX5DwLYyhdFC0WNpriATm2aWr05AfRTwP3My2j5tiBw; timezone=Asia/Shanghai; li_theme=light; li_theme_set=app; UserMatchHistory=AQJuBVEE7Lg6wQAAAYmGtCDMEeqFD21BS0F_lgZWjKp7_m9ZlM03BdgJr5HbBzLLlIBUeI0dRyznoJiI22wht_yHRrUT-4dltyNZ670vYyVc7Eob3rRQuRSF-wPFGvUPDkq0KHC9QwrWU30PNVz9ajOKgTpGMa9Juo3mNw4cDcxIFnXbZSpPH4gEDDL-EyyEOegh4WstK5Bcogaftg6oR5TD1d7CMo2rOY-Va8fkjGfvNDyiPLDkbn-WJESqIgzcrRJtnYhZ5FFBbxhGaDRaoftUOXw2FT9NFBdENpe291dKGMTGuUjBOHEKWrUNomfMpkzryRkEa2saZwjP7YwwKsyUgwklzZo; _guid=b71e630b-f7cc-4000-afb8-c7545d93c4a6; li_sugr=5de45e3f-96a4-49e0-9a5d-ea3777c2983c; AnalyticsSyncHistory=AQJg0S_t5ll3ZgAAAYmGtCDMP8js9BFGe-Y4e_Onmfk4OEo7nOOeOyGhr_oDq4SI0z27gDvPGd1vDV6bfEaVlQ; lms_ads=AQHuTA6WlDz_qAAAAYmGtCGRdHEQ5DtDiJnhmXreLuKRabtLPZmRbJGT-3K1Juq0asn4IHXhPbf-563t_bJzgFvWCAV5qyri; lms_analytics=AQHuTA6WlDz_qAAAAYmGtCGRdHEQ5DtDiJnhmXreLuKRabtLPZmRbJGT-3K1Juq0asn4IHXhPbf-563t_bJzgFvWCAV5qyri"""}
    semaphore = asyncio.Semaphore(1)
    async with aiohttp.ClientSession() as session:
        a = Application(session, _headers, semaphore)
        for index, project_id in enumerate(project_id_list):
            if index < 2020:
                continue
            logger.info(index)
            time.sleep(3)
            await a.get_applicant_list_by_(project_id)
        # await asyncio.gather(*[a.get_applicant_list_by_(project_id)
        #     for project_id in project_id_list
        # ])
if __name__ == '__main__':
    asyncio.run(run())