import yfinance as yf
import numpy as np 
from indicators.indicators import Indicators
import time
import csv 
from datetime import datetime
import pandas as pd
from binance.spot import Spot
import requests
import ccxt
from data import Database
import random

class EMAXMACD(Indicators, Database):

    # Enter long trades when MACD[0] cross MACD[1] if they are below 0, to gain more confidence consider EMA200
    # consider enter long if EMA200 is below price line

    # Enter shorts when MACD[0] > MACD[1] and MACD[0] crosses MACD[1] and becomes MACD[0] < MACD[0] also the values must be above 0
    # consider enter short if EMA200 is above the price  

    def __init__(self, pair, timeframe, checkingPeriodMin,client, risk_Ratio=[0.5,-0.75]):
        self.pair = pair
        
   
        self.binPair = self.pair.replace("-", "").replace("USD", "USDT")
        self.timeFrame = timeframe # support only for 1m 3m 5m 10m 15m 1h 4h 1d 7d
        self.checkingPeriodMin = checkingPeriodMin  # this value is for how often should check for recheck indicators and ongoing trades

        self.exchange = ccxt.binance()

        self.direction = None 
        self.MACDXEMA_History = np.empty(shape=(0,3), dtype=float) # 0 - MACD 1 - Signal Line 2 - EMA holds upto maximum of 100 MACD values. give timeFrame may affect this (example - if timeframe is low this only contains values for very shorter period)
        self.activeTrade = False
        
        self.TP = risk_Ratio[0]
        self.SL = risk_Ratio[1]

        self.client = client

        self.tradeSize = 100
        self.pastMacd = np.array([])

        self.backAddress = "http://20.106.210.106:3000"
        self.tradeid = ''


        # entry pnl pnl_percent macd macd_signal ema
        self.currentTradeData = {
            "entry" : None, 
            "side": None,
            "sizeFiat" : None,
            "sizeAsset" : None,
            "pnl" : None,
            "pnl_percent" : None,
            "macd" : None,
     
            "ema" : None,
            "entry_time" : None,
            "timeframe" : self.timeFrame,
            "pair" : self.pair,
            "tradeid" : ''
        }

        prev = self.checkCurrentTrade(self.pair, self.timeFrame)

        if (prev[0]):
            self.currentTradeData = prev[1][0]
            self.activeTrade = True
            print("Found Previous Trade")
        else: 
            self.clearCurrentTrade()
            pass

    def calculatePNL(self):
        if self.activeTrade:
            entry = float(self.currentTradeData["entry"])
            side = self.currentTradeData["side"]
            sizeFiat = self.currentTradeData["sizeFiat"]
            sizeAsset = self.currentTradeData["sizeAsset"]
            
            if side == "LONG": 
                pnl = (self.getPrice() - entry) * sizeAsset # Z (X-Y) = xy - yz
                pnl_percent = (self.getPrice() - entry) / entry * 100
            elif side == "SHORT":
                pnl = (entry - self.getPrice()) * sizeAsset
                pnl_percent = (entry - self.getPrice()) / entry * 100
            

            self.currentTradeData["pnl"] = pnl
            self.currentTradeData["pnl_percent"] = pnl_percent
            
            print("----------------------------------------")
            print(self.pair)
            print(self.currentTradeData)
            print("----------------------------------------")

    def saveTrade(self):
        col_names = ["entry", "exit", "side", "sizeFiat", "sizeAsset", "pnl", "pnl_percent", "macd", "ema","macd_exit", "ema_exit", "entry_time", "exit_time", "timefram", "pair"]
        MACD = self.MACD()
        EMA = self.EMA(200)

        data = {
            "entry" : self.currentTradeData["entry"],
            "exit" : self.getPrice(),
            "side" : self.currentTradeData["side"],
            "sizeFiat" : self.currentTradeData["sizeFiat"],
            "sizeAsset" : self.currentTradeData["sizeAsset"],
            "pnl" : self.currentTradeData["pnl"],
            "pnl_percent" : self.currentTradeData["pnl_percent"],
            "macd" : self.currentTradeData["macd"],
            "ema" : self.currentTradeData["ema"],
            "macd_exit" : MACD,
            "ema_exit" : EMA,
            "entry_time" : self.currentTradeData["entry_time"],
            "exit_time" : self.getDateTime(),
            "timefram" : self.timeFrame,
            "pair" : self.pair
        }

        self.saveTradeToDatabase(data)


        with open("trades.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=col_names)
            writer.writerow(data)

        print(f"\n Trade Completed on {self.pair} - {self.timeFrame}")
        print(data)
        print("----------------------------------------------")

    def exitTrade(self):
        MACD = self.MACD()

        if self.activeTrade:
            if self.currentTradeData["pnl_percent"] > self.TP:
                print("TP Hit !")
                
                self.saveTrade()
                self.activeTrade = False
                self.clearCurrentTrade()
            elif self.currentTradeData["pnl_percent"] < self.SL:
                print("SL Hit !")
                
                self.saveTrade()
                self.activeTrade = False
                self.clearCurrentTrade()
            
            elif MACD < -5 and self.currentTradeData['side'] == "LONG":
                self.saveTrade()
                self.activeTrade = False 
                self.clearCurrentTrade()

                self.enterTrade("SHORT")
            
            elif MACD > 5 and self.currentTradeData['side'] == "SHORT":
                self.saveTrade()
                self.activeTrade = False
                self.clearCurrentTrade()

                self.enterTrade("LONG")

    def enterTrade(self, side):
        price = self.getPrice()
        MACD = self.MACD()
        EMA = self.EMA(200)

        if side == 'LONG':
            self.tradeid = "TRD-LONG-" + str(random.randint(1, 9999))
            self.currentTradeData = {
            "entry" : price, 
            "side": "LONG",
            "sizeFiat" : self.tradeSize,
            "sizeAsset" : self.tradeSize / price,
            "pnl" : 0,
            "pnl_percent" : 0,
            "macd" : MACD,
            "ema" : EMA,
            "entry_time" : datetime.now(),
             "timeframe" : self.timeFrame,
            "pair" : self.pair,
            "tradeid"  : self.tradeid
            }
        elif side == 'SHORT':
            self.tradeid = "TRD-SHORT-" + str(random.randint(1, 9999))
            self.currentTradeData = {
            "entry" : price, 
            "side": "SHORT",
            "sizeFiat" : self.tradeSize,
            "sizeAsset" : self.tradeSize / price, 
            "pnl" : 0,
            "pnl_percent" : 0,
            "macd" : MACD,
            "ema" : EMA,
            "entry_time" : datetime.now(),
            "timeframe" : self.timeFrame,
            "pair" : self.pair,
            "tradeid"  : self.tradeid
            }

        self.activeTrade = True
        self.currentTradeData["entry_time"] = self.getDateTime()
        print(f"Trade Entered : {side} at {price}")
        self.newCurrentTrade(self.currentTradeData)
        self.calculatePNL()
        print(self.currentTradeData)

    def saveLastUpdated(self):
        dt = datetime.now()

        with open("./Temp/last.txt", "w") as file:
            file.write(str(dt))
            data = str(dt)

            p = requests.post(self.backAddress+"/lastUpdated", json={"value" : data})
            
    def getDateTime(self):
        now = datetime.now()

        # Format the date and time
        date = now.strftime("%Y-%m-%d %H:%M:%S")

        return date

    def trade(self):
        
        while True:
            
            try:
                self.saveLastUpdated()

                price = self.getPrice()
                MACD = self.MACD()
                EMA = self.EMA(200)

                self.pastMacd= np.append(self.pastMacd, MACD)
                if len(self.pastMacd) > 50:
                    self.pastMacd = np.delete(self.pastMacd, 0)

                if self.activeTrade:
                    self.calculatePNL()
                    self.exitTrade()


                if (len(self.pastMacd) > 3):
                        
                    # Enter Long Trade
                    # 1. MACD[-2] should be minus value and MACD[-1] SHOULD be 10<
                    # 2. EMA Should be less than price

                    print(f"Looking for trade {self.pair} in {self.timeFrame}")

                    print(f"MACD[-2] : {self.pastMacd[-2]} / MACD[-1] : {self.pastMacd[-1]}")
          
                    print()

                    if (self.pastMacd[-2] < 0) and (self.pastMacd[-1] > 0) and self.activeTrade == False:
                        self.enterTrade("LONG")
                        print(f"Long Trade Entered {self.pair} - {self.timeFrame}")
                    
                
                    # Enter Short Trade
                    # 1. MACD[-2] should be plus value and MACD[-1] SHOULD be -10<
                    # 2. EMA Should be greater than price

                    if (self.pastMacd[-2] > 0) and (self.pastMacd[-1] < 0) and self.activeTrade == False:
                        self.enterTrade("SHORT")
                        print(f"Short Trade Entered {self.pair} - {self.timeFrame}")

                    
                if self.activeTrade:
                    self.calculatePNL()
                    self.exitTrade()
                
                time.sleep(60)
            
            except Exception as e:
                print(f"Error in {self.pair} - {self.timeFrame} \n{e}")
                print("Retrying in 10 seconds...")
                time.sleep(10)
          