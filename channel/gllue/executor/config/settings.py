import json
import os


class Settings:
    # 正式环境
    tip_app_config = {
        "ConvertServerHost": os.getenv("ConvertServerHost", "http://localhost:64994"),
        "TipTransmitterServerHost": os.getenv("TipTransmitterServerHost", "http://ruleengine.mesoor.com"),
        "StoreDerivationServerHost": os.getenv("StoreDerivationServerHost", "http://localhost:62848"),
         "TipSpaceServerHost": os.getenv("TipSpaceServerHost", "http://localhost:51413")
    }
    # print(tip_app_config)

    # 测试环境
    # tip_app_config = {
    #     "ConvertServerHost": os.getenv("ConvertServerHost", "http://localhost:54635"),
    #     "TipTransmitterServerHost": os.getenv("ConvertServerHost", "http://ruleengine.nadileaf.com"),
    #     "StoreDerivationServerHost": os.getenv("ConvertServerHost", "http://localhost:61505"),
    #     "TipSpaceServerHost": os.getenv("ConvertServerHost", "http://localhost:63579")
    # }


