import json
import urllib
from urllib import request, parse
from urllib.parse import urlencode
body = {"candidateexperience_set":[{"client":{"name":"mesoor-test9","id":None},"is_current":True,"gllueext_text_1580804429654":"","gllueext_achievements":"","department":None}],"type":"candidate","candidateproject_set":[],"candidateeducation_set":[],"candidatelanguage_set":[],"chineseName":"测试","englishName":"","owner":2491,"gllueext_select_1532920743234":"","gllueext_channelURL":"","gllueext_Summary":"","gllueext_text_miaoshu":"","noticeData":{"model":"candidate","notices":[]},"joborder":146902,"mobile":"17612305721","locations":"88","email":"723883101@qqq.com","mobile1":"","functions":"25","industrys":"134","channel":"400000","_notice_data":[]}
import requests
iii = "data="+parse.quote(json.dumps(body, ensure_ascii=False))
url = "http://www.cgladvisory.com/rest/candidate/add"

payload = "data=%7B%22candidateexperience_set%22%3A%5B%7B%22client%22%3A%7B%22name%22%3A%22mesoor-test9%22%2C%22id%22%3Anull%7D%2C%22is_current%22%3Atrue%2C%22gllueext_text_1580804429654%22%3A%22%22%2C%22gllueext_achievements%22%3A%22%22%2C%22department%22%3Anull%7D%5D%2C%22type%22%3A%22candidate%22%2C%22candidateproject_set%22%3A%5B%5D%2C%22candidateeducation_set%22%3A%5B%5D%2C%22candidatelanguage_set%22%3A%5B%5D%2C%22chineseName%22%3A%22%E6%B5%8B%E8%AF%95%22%2C%22englishName%22%3A%22%22%2C%22owner%22%3A2491%2C%22gllueext_select_1532920743234%22%3A%22%22%2C%22gllueext_channelURL%22%3A%22%22%2C%22gllueext_Summary%22%3A%22%22%2C%22gllueext_text_miaoshu%22%3A%22%22%2C%22noticeData%22%3A%7B%22model%22%3A%22candidate%22%2C%22notices%22%3A%5B%5D%7D%2C%22joborder%22%3A146902%2C%22mobile%22%3A%2217612305721%22%2C%22locations%22%3A%2288%22%2C%22email%22%3A%22723883101%40qqq.com%22%2C%22mobile1%22%3A%22%22%2C%22functions%22%3A%2225%22%2C%22industrys%22%3A%22134%22%2C%22channel%22%3A%22400000%22%2C%22_notice_data%22%3A%5B%5D%7D"

print(payload)
print(iii)


# headers = {
#   'Accept': 'application/json, text/plain, */*',
#   'Accept-Language': 'zh-CN,zh;q=0.9',
#   'Cache-Control': 'no-cache',
#   'Connection': 'keep-alive',
#   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#   'Origin': 'https://www.cgladvisory.com',
#   'Pragma': 'no-cache',
#   'Referer': 'https://www.cgladvisory.com/crm/client/list?gql=keyword%3Dtest&page=1',
#   'Sec-Fetch-Dest': 'empty',
#   'Sec-Fetch-Mode': 'cors',
#   'Sec-Fetch-Site': 'same-origin',
#   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#   'b3': '3162f51a6e6088b2401434ff30c9dbae-9b848b0305e738af-1',
#   'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
#   'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"macOS"',
# "gllue_private_token":"SC03NF%2BgD3Q/3wU26ELQmB90DXATbWHvdM%2BkLixvqbrTiziyllROexSwVvDXktsF%0A"
# }
#
# response = requests.request("POST", url, headers=headers, data=encoded_data)
#
# print(response.text)
