import requests
import json

from loguru import logger


def get_candidate_info(candidate_id: str, headers: dict):

    url = f"http://www.linkedin.com/talent/api/talentLinkedInMemberProfiles/urn:li:ts_linkedin_member_profile:({candidate_id},1,urn:li:ts_hiring_project:0)"

    data = "altkey=urn&decoration=%28entityUrn%2CreferenceUrn%2Canonymized%2CunobfuscatedFirstName%2CunobfuscatedLastName%2CmemberPreferences%28availableStartingAt%2Clocations%2CgeoLocations*~%28standardGeoStyleName%29%2CopenToNewOpportunities%2Ctitles%2CinterestedCandidateIntroductionStatement%2Cindustries*~%2CcompanySizeRange%2CemploymentTypes%2CproxyPhoneNumberAvailability%2Cbenefits%2Cschedules%2CsalaryLowerBounds%2Ccommute%2CjobSeekingUrgencyLevel%2CopenToWorkRemotely%2ClocalizedWorkplaceTypes%2CremoteGeoLocationUrns*~%28standardGeoStyleName%29%29%2CfirstName%2ClastName%2Cheadline%2Clocation%2CprofilePicture%2CvectorProfilePicture%2CnumConnections%2Csummary%2CnetworkDistance%2CprofileSkills*%28name%2CskillAssessmentBadge%2CprofileResume%2CendorsementCount%2CprofileSkillAssociationsGroupUrn~%28entityUrn%2Cassociations*%28description%2Ctype%2CorganizationUrn~%28name%2Curl%2Clogo%29%29%29%2ChasInsight%29%2CpublicProfileUrl%2CcontactInfo%2Cwebsites*%2CcanSendInMail%2Cunlinked%2CunLinkedMigrated%2Chighlights%28connections%28connections*~%28entityUrn%2CfirstName%2ClastName%2Cheadline%2CprofilePicture%2CvectorProfilePicture%2CpublicProfileUrl%2CfollowerCount%2CnetworkDistance%2CautomatedActionProfile%29%2CtotalCount%29%2Ccompanies%28companies*%28company~%28followerCount%2Cname%2Curl%2CvectorLogo%29%2CoverlapInfo%29%29%2Cschools%28schools*%28school~%28name%2Curl%2CvectorLogo%29%2CschoolOrganizationUrn~%28name%2Curl%2Clogo%29%2CoverlapInfo%29%29%29%2CfollowingEntities%28companies*~%28followerCount%2Cname%2Curl%2CvectorLogo%29%2Cinfluencers*~%28entityUrn%2CfirstName%2ClastName%2Cheadline%2CprofilePicture%2CvectorProfilePicture%2CpublicProfileUrl%2CfollowerCount%2CnetworkDistance%2CautomatedActionProfile%29%2Cschools*~%28name%2Curl%2CvectorLogo%29%2CschoolOrganizationsUrns*~%28name%2Curl%2Clogo%29%29%2Ceducations*%28school~%28name%2Curl%2CvectorLogo%29%2CorganizationUrn~%28name%2Curl%2Clogo%29%2CschoolName%2Cgrade%2Cdescription%2CdegreeName%2CfieldOfStudy%2CstartDateOn%2CendDateOn%29%2CgroupedWorkExperience*%28companyUrn~%28followerCount%2Cname%2Curl%2CvectorLogo%29%2Cpositions*%28title%2CstartDateOn%2CendDateOn%2Cdescription%2Clocation%2CemploymentStatus%2CorganizationUrn%2CcompanyName%2CassociatedProfileSkillNames%2CcompanyUrn~%28url%2CvectorLogo%29%29%2CstartDateOn%2CendDateOn%29%2CvolunteeringExperiences*%28company~%28followerCount%2Cname%2Curl%2CvectorLogo%29%2CcompanyName%2Crole%2CstartDateOn%2CendDateOn%2Cdescription%29%2Crecommendations*%28recommender~%28entityUrn%2CfirstName%2ClastName%2Cheadline%2CprofilePicture%2CvectorProfilePicture%2CpublicProfileUrl%2CfollowerCount%2CnetworkDistance%2CautomatedActionProfile%29%2CrecommendationText%2Crelationship%2Ccreated%29%2Caccomplishments%28projects*%28title%2Cdescription%2Curl%2CstartDateOn%2CendDateOn%2CsingleDate%2Ccontributors*%28name%2ClinkedInMember~%28entityUrn%2Canonymized%2CunobfuscatedFirstName%2CunobfuscatedLastName%2CfirstName%2ClastName%2Cheadline%2CprofilePicture%2CvectorProfilePicture%2CpublicProfileUrl%2CfollowerCount%2CnetworkDistance%2CautomatedActionProfile%29%29%29%2Ccourses*%2Clanguages*%2Cpublications*%28name%2Cpublisher%2Cdescription%2Curl%2CdateOn%2Cauthors*%28name%2ClinkedInMember~%28entityUrn%2Canonymized%2CunobfuscatedFirstName%2CunobfuscatedLastName%2CfirstName%2ClastName%2Cheadline%2CprofilePicture%2CvectorProfilePicture%2CpublicProfileUrl%2CfollowerCount%2CnetworkDistance%2CautomatedActionProfile%29%29%29%2Cpatents*%28number%2CapplicationNumber%2Ctitle%2Cissuer%2Cpending%2Curl%2CfilingDateOn%2CissueDateOn%2Cdescription%2Cinventors*%28name%2ClinkedInMember~%28entityUrn%2Canonymized%2CunobfuscatedFirstName%2CunobfuscatedLastName%2CfirstName%2ClastName%2Cheadline%2CprofilePicture%2CvectorProfilePicture%2CpublicProfileUrl%2CfollowerCount%2CnetworkDistance%2CautomatedActionProfile%29%29%29%2CtestScores*%2Chonors*%2Ccertifications*%28name%2ClicenseNumber%2Cauthority%2Ccompany~%28followerCount%2Cname%2Curl%2CvectorLogo%29%2Curl%2CstartDateOn%2CendDateOn%29%29%2CprivacySettings%28allowConnectionsBrowse%2CshowPremiumSubscriberIcon%29%2ClegacyCapAuthToken%2CfullProfileNotVisible%2CcurrentPositions*%28company~%28followerCount%2Cname%2Curl%2CvectorLogo%29%2CcompanyName%2Ctitle%2CstartDateOn%2CendDateOn%2Cdescription%2Clocation%29%2CindustryName%29"
    res = requests.post(url=url, headers=headers, data=data)
    try:
        if res.status_code == 200 and "contactInfo" in res.json().keys():
            body = res.json()
            body["candidateId"] = candidate_id
            with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate.jsonl", "a") as f:
                f.write(json.dumps(body, ensure_ascii=False)+'\n')
        else:
            logger.error(f"{res.content.decode()}")
            logger.error(candidate_id)
            logger.error(res.status_code)
    except Exception as e:
        print(res.json())


if __name__ == '__main__':
    headers = {
        'authority': 'www.linkedin.com',
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'bcookie="v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3"; bscookie="v=1&20230625131234c1ec8eca-ffde-440f-8995-f02159c714c0AQGY-egn1l-MvsO24lLgd6XuCc57BNDW"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19534%7CvVersion%7C5.1.1; _gcl_au=1.1.60394227.1687700073; liap=true; JSESSIONID="ajax:8187577550675074642"; li_a=AQJ2PTEmY2FwX3NlYXQ9MTM5NTQzMTkzJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTGOduw-vgZXLHTN1eTVyNG00jjSpg; cap_session_id=4355459411:1; li_er=v=1&r=urn:li:contract:207833291&t=1685998288304&g=MDIx6GM5iIj+Le1ifRGiwh7FdRUIB7b97ep1EHGhLFe1t2M=; u_tz=GMT+0800; li_sugr=5712ddf1-2e1a-41bb-8603-e4f30e555ec0; timezone=Asia/Shanghai; li_theme=light; li_theme_set=app; _guid=fc3c4854-ad38-4420-b0dd-1bbe435829a9; UserMatchHistory=AQJbtonmgs7oowAAAYlD_gQJlujyyARu9yzulQVWOYICRX6kvqDOCMfieqJKH6YafxATvmBYyxab7Vxh_m6DiWq7c91CxCGb34xZQ8Wf-Dp4OfAWMeeo200QXcFTZ3Yo7JW6_R_tr2UxyPIQKxGwLT9xKjBMdUNLEVwT-3Q2ZjY6jfr4Gmem9X1uSHmQAxyFUfrjvr2QIis4fhNpf3LzZdh7enS0XjITml-Hk1515p4U4N7t8XdT1CaUavlqvCuKCdlJR8Ehk0dOA8aMKiTwjDxEwqdtUienqoW04VFEKlJMyzo-_nkmf60BhGgGGA-GM5Ue5z0QFAiQ0j3Lg870cpECfmgs-84; AnalyticsSyncHistory=AQI9Eux7GDhv8AAAAYlD_gQJf3k4gFChNeGTK1txbXRdTBhsHTY3zTlMXfy1bHLhYG5fXX_cNY0Kjhf3uTIEQA; lms_ads=AQEZ-uIqDo4HSgAAAYlD_gUR8SJ5Rb13Z7jItJoRpZ_ilBY2-zT0nKTIJXpErnvzKXyj5nQfj9k1iUdNzCYGToQZU_LRTnx6; lms_analytics=AQEZ-uIqDo4HSgAAAYlD_gUR8SJ5Rb13Z7jItJoRpZ_ilBY2-zT0nKTIJXpErnvzKXyj5nQfj9k1iUdNzCYGToQZU_LRTnx6; lang=v=2&lang=zh-cn; lidc="b=OB81:s=O:r=O:a=O:p=O:g=2877:u=300:x=1:i=1689734513:t=1689817081:v=2:sig=AQGd5__LmXYaR8rFY88rtsrvPaw0DAom"; li_at=AQEDAQfs8hUAeo8kAAABiPLVdbAAAAGJkBMHs1YAzIEeNmzUzpSmCyFcg57R_12Gnisrtabp-jQMJvWFbx7zfp7pwO8WTVqUl4_aQOC6e2SFT_jzuZ8ayCY4KVM_anBjUjoazxUEmLCoR1oDnc_YwR6O; bcookie="v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3"',
        'cookie': """bcookie="v=2&03829025-dc94-4f5e-8f6d-ff30180f0100"; bscookie="v=1&202302240242576cf1d9f5-7908-43f0-8fbb-4c1d1015fbd8AQETlEXRwp5JiDkpTuh_wwCtV41g4gMT"; lang=v=2&lang=zh-cn; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19530%7CMCMID%7C05115440129191921120818389973139956633%7CMCAAMLH-1687915423%7C11%7CMCAAMB-1687915423%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1687317823s%7CNONE%7CvVersion%7C5.1.1; at_check=true; li_gc=MTswOzE2ODczMTA2MjM7MjswMjG89eUvw/o+1mWWmUeniKW48YJ/r7e9yM0lrL9t1x/o+w==; mbox=session#521eb3e9f2a1418e819a66242a8fa445#1687312485|PC#521eb3e9f2a1418e819a66242a8fa445.32_0#1702862625; gpv_pn=business.linkedin.com%2Fzh-cn%2Ftalent-solutions%2Fs%2F05301%2Fmetaverse_recruit; s_ips=1250; s_tp=2258; s_ppv=business.linkedin.com%2Fzh-cn%2Ftalent-solutions%2Fs%2F05301%2Fmetaverse_recruit%2C55%2C55%2C1250%2C1%2C1; s_tslv=1687310624262; s_cc=true; _gcl_au=1.1.1841983647.1687310624; li_sugr=ed4f1eb3-8a02-4c4c-9832-8e171c4692d6; li_at=AQEDATfO7VQCtD8uAAABiYcMqnwAAAGJqxkufFYAxw_ToAsWYsQbj0J7hkKTwpvMxFpRZ6RM_Vynec0L4QAUD4IHtL4_v_lbugJjFaUkRHUPgovXA2xzJNOk8W7GAqq8iEgAkujI6vZLVVRzCPCC-iKk; liap=true; JSESSIONID="ajax:0009957110063883094"; lidc="b=OB52:s=O:r=O:a=O:p=O:g=3407:u=27:x=1:i=1690187901:t=1690271074:v=2:sig=AQHyWU8e8CHG318_QPMOGH4xoYFk2-4V"; li_cc=AQFSEvratAlKqgAAAYmHDLo9tjig4EcGdVZ2UmNKU7rCfLFr9_v_HeW1slgRmKpIacRSgIFJ32L5; li_a=AQJ2PTEmY2FwX3NlYXQ9MjU3NjU2NzYxJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTFLvei1v8lDjAZtRU-MxcY48ro9kQ; cap_session_id=4387742541:1; li_er=v=1&r=urn:li:contract:207833291&t=1688484934268&g=MDIxplFkRN2w/cTJ8jFDIqXPjuDK7X6nvdcNICqDD7AZNBM=; sdsc=35%3A1%2C1690184797330%7ECAOR%2C0%7ECAST%2C32458300PF%2FrDZ%2BbaLXAvDVcEhPi0Ihr48%3D; u_tz=GMT+0800""",
        # 'csrf-token': 'ajax:8187577550675074642',
        'csrf-token': 'ajax:0009957110063883094',
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
    get_candidate_info("AEMAABeAaaQBMrbkUXqIgIQGdcADQLsUwe0Jja4",headers)
