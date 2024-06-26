import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

class Database:

    def __init__(self):
        pass

    def updateCurrentTrade(self, trade_data):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = conn.cursor()

        self.cursor.execute('''
            INSERT INTO currentTradeData (
                entry, side, sizeFiat, sizeAsset, pnl, pnl_percent, macd, macd_signal, ema, entry_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade_data["entry"],
            trade_data["side"],
            trade_data["sizeFiat"],
            trade_data["sizeAsset"],
            trade_data["pnl"],
            trade_data["pnl_percent"],
            trade_data["macd"],
            trade_data["macd_signal"],
            trade_data["ema"],
            trade_data["entry_time"]
        ))
    
        conn.commit()
        conn.close()
    
    def saveTradeToDatabase(self, data):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO trades (
                entry, exit, side, sizeFiat, sizeAsset, pnl, pnl_percent, macd, ema, macd_exit, ema_exit, entry_time, exit_time, timefram, pair
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            data["pair"]
        ))
        
        conn.commit()
        conn.close()
        
        print("Trade Saved ! ")

    def clearCurrentTrade(self):
        conn = sqlite3.connect('data.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("delete from currentTradeData")
        
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
            "macd", "macd_signal", "ema", "entry_time"
        ]
        
        # Convert fetched data to a list of dictionaries
        trade_data_list = []
        for row in data:
            trade_data = dict(zip(column_names, row))
            trade_data_list.append(trade_data)
        
        conn.close()

        if (bool(data)):
            

            print("Continuing Previous Trade...")
            return [True, trade_data_list]
        else:
            conn.close()
            print("No Previous ongoing Trades Found ! ")
            return [False, []]

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