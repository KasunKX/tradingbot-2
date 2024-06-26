import yfinance as yf
import numpy as np
import ccxt
import pandas as pd
import ta

class Indicators:
    def __init__(self, pair, timeFrame, checkingPeriodMin):
        self.pair = pair 
        self.timeFrame = timeFrame
        self.checkingPeriodMin = checkingPeriodMin
        self.exchange = ccxt.binance()
    
    def MACD(self):
        ohlcv = self.exchange.fetch_ohlcv(self.binPair, self.timeFrame, limit=50)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')


        # Calculate MACD
        df['MACD'] = ta.trend.macd(df['close'])
        df['MACD_Signal'] = ta.trend.macd_signal(df['close'])
        df['MACD_Hist'] = ta.trend.macd_diff(df['close'])

        MACD = df['MACD_Hist'].iloc[-1]

        return round(MACD, 1)
    
    
    def EMA(self, emaLen, period="1mo"):
        pair = yf.Ticker(self.pair)
        data = pair.history(period=period, interval=self.timeFrame)
        data["EMA"] = data["Close"].ewm(span=emaLen, adjust=False).mean()
        ema = data["EMA"]
        return round(ema.iloc[-1], 1)
    
    
    def getPrice(self):

        # print(self.binPair)
        return round(float(self.client.ticker_price(self.binPair).get('price')), 1)
