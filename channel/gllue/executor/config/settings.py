import os
class Settings:
    tip_app_config = {
        "ConvertServerHost": os.getenv("ConvertServerHost", "http://localhost:64994"),
        "TipTransmitterServerHost": os.getenv("TipTransmitterServerHost", "http://localhost:57978"),
        "StoreDerivationServerHost": os.getenv("StoreDerivationServerHost", "http://localhost:62848"),
         "TipSpaceServerHost": os.getenv("TipSpaceServerHost", "http://localhost:51413")
    }
    print(tip_app_config)
    # tip_app_config = {
    #     "ConvertServerHost": os.getenv("ConvertServerHost", "http://localhost:54635"),
    #     "TipTransmitterServerHost": os.getenv("ConvertServerHost", "http://localhost:53740"),
    #     "StoreDerivationServerHost": os.getenv("ConvertServerHost", "http://localhost:61505"),
    #     "TipSpaceServerHost": os.getenv("ConvertServerHost", "http://localhost:63579")
    # }