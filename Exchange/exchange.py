from binance.um_futures import UMFutures 

apiKey = "byELXxnUrWAjtlZAWQCZ29mYaKXEgT0AKSiLc43mJHrwpuh8EpQW8piDoSefVKzX"
Secret = "VBWPOyzstF6WWxevrNeezumQFZVTxPw7Fgkk1sBj3VRwvmX3ahgSw72aB2hSBgUE"

class Exchange:

    def __init__(self):
        self.cm_futures_client = UMFutures(key=apiKey, secret=Secret)
    
    def account(self):
        data = self.cm_futures_client.account()['assets']
      
        USDT = []
        
        for i in data:
            if i["asset"] == "USDT":
                USDT = i 

        print(USDT)
        # print(data)


a = Exchange()
a.account()