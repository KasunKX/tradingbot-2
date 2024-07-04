from binance.um_futures import UMFutures 
import logging

apiKey = "byELXxnUrWAjtlZAWQCZ29mYaKXEgT0AKSiLc43mJHrwpuh8EpQW8piDoSefVKzX"
Secret = "VBWPOyzstF6WWxevrNeezumQFZVTxPw7Fgkk1sBj3VRwvmX3ahgSw72aB2hSBgUE"

class Exchange:

    def __init__(self):
        self.client = UMFutures(key=apiKey, secret=Secret)
    
    def account(self):
        data = self.client.account()['assets']
      
        USDT = []
        
        for i in data:
            if i["asset"] == "USDT":
                USDT = i 

        print(USDT)
        # print(data)
    
    def PlaceTrade(self, side):
        response = self.client.new_order_test(
        symbol="BTCUSDT",
        side="SELL" if side == "SHORT" else "BUY",
        type="MARKET",
        quantity=120,
        )

        print(response)

        logging.info(response)


a = Exchange()
a.PlaceTrade("SHORT")