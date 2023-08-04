import time

from selenium import webdriver

driver = webdriver.Chrome()
cookie_list = {
    "bcookie":"\"v=2&eef38a30-d58a-40a5-828b-07eaaab23dd3\"",
    "bscookie":"\"v=1&20230625131234c1ec8eca-ffde-440f-8995-f02159c714c0AQGY-egn1l-MvsO24lLgd6XuCc57BNDW\"",
    "_gcl_au":"1.1.60394227.1687700073",
    "liap":"true",
    "JSESSIONID":"\"ajax:8187577550675074642\"",
    "u_tz":"GMT+0800",
    "li_sugr":"5712ddf1-2e1a-41bb-8603-e4f30e555ec0",
    "timezone":"Asia/Shanghai",
    "li_theme":"light",
    "li_theme_set":"app",
    "_guid":"fc3c4854-ad38-4420-b0dd-1bbe435829a9",
    "gpv_pn":"business.linkedin.com%2Fzh-cn%2Fproduct-sign-in",
    "li_ep_auth_context":"AExhcHA9YWNjb3VudENlbnRlcixhaWQ9MjI5OTE0NixpaWQ9LTEscGlkPTE0MDY4ODAzLGV4cD0xNjkwMTkzNTMzMjU3LGN1cj10cnVlAZ61FoeCFmW6c-i9JOZdCh4yYUYv",
    "aam_uuid":"04603882441184570594441513473932382631",
    "s_ips":"823",
    "s_tslv":"1690164765958",
    "s_tp":"1488",
    "mbox":"PC#71c1d85d0ee743d181b2c1e37465dc0c.32_0#1705716767|session#af7350565aea436e863791f9c1e2fd29#1690166627",
    "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg":"-637568504%7CMCIDTS%7C19563%7CvVersion%7C5.1.1%7CMCMID%7C04809171412315487124425987044269564524%7CMCAAMLH-1690788841%7C11%7CMCAAMB-1690788841%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1690191241s%7CNONE%7CMCCIDH%7C-894394514",
    "li_a":"AQJ2PTEmY2FwX3NlYXQ9MTM5NTQzMTkzJmNhcF9hZG1pbj10cnVlJmNhcF9rbj0yMDc4MzMyOTF5PSiCB_HcVsjGxRzTj0R1q7-QNA",
    "cap_session_id":"4387653641:1",
    "li_er":"v=1&r=urn:li:contract:207833291&t=1688481207464&g=MDIxTpf7S3ooI/Fx/MCKO/rPJ6kx7oPdUA7sQ8jKON68KSg=",
    "lang":"v=2&lang=zh-cn",
    "UserMatchHistory":"AQK4rPZjeMfgRwAAAYmu815v_XPfq9_ONm5EHHrTcuzt4JAWYMp8Oz34C9rhsVac3DsoclciID0c0p6-KZkHvYLpgoid8VwVE6jXC5JK9lnd66Lu8mVXuWh_6Hz3qzVWagLMpWoqqS2TLh033rtlwyS5LzamneJ40BEG6CUgXRxZjh1MHE_NMY3FybaAzAvX28hEEXR8pOIRoKgrJRCi3mowcqCHLQDKwyZrAyJAWRXqi8IrEAeVHS2BHprDBPjHmhPHdRSwLDyVLTWG-m7TceD-Fv7HhdTw7QEv0_nmWgAqnZ-_nLn57_J2OZKzlxyXBJ4Bm4arW5IgBCM9Ps9Z8AUJVD9V6is",
    "AnalyticsSyncHistory":"AQIJajRIqJ7YgwAAAYmu815w7QqXYHf0keh1xW8ijSXzhkWhGu2Sjv-2DGqat18-7dlMekpE-rnexpTgvVXMyw",
    "lms_ads":"AQGqZoHMibmXngAAAYmu82CJJHBW7KunU5pbgwtKhx7tdvyMXrT-YgEilZZBtt2jGa3oX5O4lPYd-Czw9CALKsb9x3KFIoJa",
    "lms_analytics":"AQGqZoHMibmXngAAAYmu82CJJHBW7KunU5pbgwtKhx7tdvyMXrT-YgEilZZBtt2jGa3oX5O4lPYd-Czw9CALKsb9x3KFIoJa",
    "li_at":"AQEFAHQBAAAAAAvwz_cAAAGJhtPMqAAAAYnTt2LRVgAAF3VybjpsaTptZW1iZXI6MTMyOTY4OTgxRLiU6FuP4s4UZPuh2st5QjdQiyeJ93lSgNzkbSUzTt4MDcHwzKOnsQFeTyiTxcu0iGcV1cQvuIMb2nRgJibBjUth9o58rYhQ09KmGAUi-Xpp1d5FhtAVqY9ZcvV4bZfxg2TWqr64a-Wf_NqAwl4llbOr8rk7W_wGtkfAATvn_s1AIsbYB-UmgNYtYWDgIzUnIAWXdA",
    "sdsc":"1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D",
    "lidc":"\"b=OB81:s=O:r=O:a=O:p=O:g=2886:u=306:x=1:i=1691043208:t=1691117608:v=2:sig=AQEgAzhkEjEQjaCHwyNNzfg-R3kR4f4S\""
}

print(cookie_list)

driver.get("https://www.linkedin.com/talent/hire/834460852/discover/applicants?start=50")
input()
driver.get("https://www.linkedin.com/talent/hire/834460852/discover/applicants?start=50")
print(driver.get_cookies())
time.sleep(100000)


