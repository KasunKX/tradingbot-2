import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

class Database:

    def __init__(self):
        pass

    def newCurrentTrade(self, trade_data):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = conn.cursor()

        self.cursor.execute('''
            INSERT INTO currentTradeData (
                entry, side, sizeFiat, sizeAsset, pnl, pnl_percent, macd, ema, entry_time, timeframe, pair, tradeid, profitflow
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade_data["entry"],
            trade_data["side"],
            trade_data["sizeFiat"],
            trade_data["sizeAsset"],
            trade_data["pnl"],
            trade_data["pnl_percent"],
            trade_data["macd"],
            trade_data["ema"],
            trade_data["entry_time"],
            trade_data['timeframe'],
            trade_data["pair"],
            trade_data["tradeid"],
            str(trade_data["profitflow"])
        ))
    
        conn.commit()
        conn.close()
    
    def saveTradeToDatabase(self, data):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO trades (
                entry, exit, side, sizeFiat, sizeAsset, pnl, pnl_percent, macd, ema, macd_exit, ema_exit, entry_time, exit_time, timefram, pair, profitflow
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["entry"],
            data["exit"],
            data["side"],
            data["sizeFiat"],
            data["sizeAsset"],
            data["pnl"],
            data["pnl_percent"],
            data["macd"],
            data["ema"],
            data["macd_exit"],
            data["ema_exit"],
            data["entry_time"],
            data["exit_time"],
            data["timefram"],
            data['pair'],
            str(data['profitflow'])
        ))
        
        conn.commit()
        conn.close()
        
        print("Trade Saved ! ")

    def clearCurrentTrade(self, timeframe):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("delete from currentTradeData where timeframe=?", (timeframe,))
        
        conn.commit()
        conn.close()

    def checkCurrentTrade(self, pair, timeframe):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        print("Checking Previous Trades...")
   
        
        c = conn.cursor()
        c.execute("SELECT * FROM currentTradeData where pair=? and timeframe=?", (pair, timeframe))
        
        data = c.fetchall()

        
        # Column names in the same order as the SELECT statement
        column_names = [
            "entry", "side", "sizeFiat", "sizeAsset", "pnl", "pnl_percent",
            "macd",  "ema", "entry_time" ,"timeframe", "pair", "tradeid"
        ]
        
        # Convert fetched data to a list of dictionaries
        trade_data_list = []
        for row in data:
            trade_data = dict(zip(column_names, row))
            trade_data_list.append(trade_data)
        
        print(trade_data_list)
        
        conn.close()

        if (bool(data)):
            print("Continuing Previous Trade...")
            return [True, trade_data_list]
        else:
            conn.close()
            print("No Previous ongoing Trades Found ! ")
            return [False, []]
        
    def allTrades(self):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        c = conn.cursor()

        c.execute("SELECT * from trades")
        data = c.fetchall()
        return str(data)
    
    def updateCurrentTrade(self, timeframe, pnl, pnl_percent, profitflow):
        try:
            conn = sqlite3.connect('data.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("UPDATE currentTradeData set profitflow=?, pnl=?, pnl_percent=? where timeframe=?", (str(profitflow), pnl, pnl_percent, timeframe))

            conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()



data = Database()
data.checkCurrentTrade("BTC-USD", "1h")

# # Connect to SQLite database (or create it if it doesn't exist)

# # Retrieve data
# c.execute('SELECT * FROM currentTradeData')
# print(c.fetchall())  # Print all rows 

# # # Insert the values into the table
# c.execute('''
# INSERT INTO currentTradeData (entry, side, sizeFiat, sizeAsset, pnl, pnl_percent, macd, ema, entry_time, timeframe, pair)
# VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# ''', (61324.8, 'LONG', 100, 0.0016306616572740555, 0.35695183677728126, 0.34863546232518594, 0.7, 61611.6, '2024-06-26 16:22:30',"5m" ,"BTC-USD"))

# # # Commit the changes and close the connection
# conn.commit()


# c.execute("SELECT * FROM currentTradeData")

# data = c.fetchall()
# print(data)

# test = Database()
# test.checkCurrentTrade()