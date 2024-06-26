import os 
import dotenv 
from binance.spot import Spot
from main import EMAXMACD
import threading
import time


dotenv.load_dotenv()

apiKey = "byELXxnUrWAjtlZAWQCZ29mYaKXEgT0AKSiLc43mJHrwpuh8EpQW8piDoSefVKzX"
Secret = "VBWPOyzstF6WWxevrNeezumQFZVTxPw7Fgkk1sBj3VRwvmX3ahgSw72aB2hSBgUE"

client = Spot(api_key=apiKey, api_secret=Secret)

pairs = ["BTC-USD"]
timeFrames = ["5m", "1h"]

tradeObjects = []

print("Creating Trade Objects...")
# Store Objects
for i in pairs:
    for t in timeFrames:
        currentObj = EMAXMACD(pair=i, timeframe=t, client=client, checkingPeriodMin=10)
        tradeObjects.append(currentObj)

print("Starting Threads...")
# Start Threads
threads = []

for i in tradeObjects:
    threads.append(threading.Thread(target=i.trade))
    

for i in threads:
    i.start()
    time.sleep(0.1)


