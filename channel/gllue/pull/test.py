import requests

url = "https://fsgtest.gllue.net/rest/v2/attachment/download/7a27d203-673b-4072-921b-62d0c106087a?gllue_private_token=sIAOM%2BO0Em00edl2LQX11k8tYSD2XR5/8vOfJw4aDQ4%3D%0A"

payload={}
headers = {
  'authority': 'fsgtest.gllue.net',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'zh-CN,zh;q=0.9',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

with open(file="xx.pdf", mode="wb") as f:
    f.write(response.content)
