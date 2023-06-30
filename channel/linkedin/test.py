import json

from lxml import etree

xpath_rule = "//code[@id='bpr-guid-335970']/text()"
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/test/project_page_1.html","r") as f:
    project = f.read()
    html_obj = etree.HTML(project)
    _json = json.loads(html_obj.xpath(xpath_rule)[0].replace("\n","").replace(" ",""))
    _project = _json["data"]["data"]["hiringProjectsByCriteria"]["*elements"]
    print(_project)


