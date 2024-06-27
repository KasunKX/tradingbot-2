import sqlite3

# Define the data to insert
data = {
    'entry': 60942.1,
    'side': 'SHORT',
    'sizeFiat': 100,
    'sizeAsset': 0.0016409017739789078,
    'pnl': 0.0,
    'pnl_percent': 0.0,
    'macd': -1.3,
    'macd_signal': None,
    'ema': None,
    'entry_time': '2024-06-27 11:07:40',
    'timeframe': '1h',
    'pair': 'BTC-USD',
    'tradeid': 'TRD-SHORT-8786'
}

# Connect to SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS currentTradeData (
        entry TEXT,
        side TEXT,
        sizeFiat REAL,
        sizeAsset REAL,
        pnl REAL,
        pnl_percent REAL,
        macd REAL,
        macd_signal REAL,
        ema REAL,
        entry_time TEXT,
        timeframe TEXT,
        pair TEXT,
        tradeid TEXT primary key
    )
''')

# Insert data into the table
cursor.execute('''
    INSERT INTO currentTradeData (
        entry, side, sizeFiat, sizeAsset, pnl, pnl_percent, macd,
        macd_signal, ema, entry_time, timeframe, pair, tradeid
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    str(data['entry']), data['side'], data['sizeFiat'], data['sizeAsset'],
    data['pnl'], data['pnl_percent'], data['macd'], data['macd_signal'],
    data['ema'], data['entry_time'], data['timeframe'], data['pair'], data['tradeid']
))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted successfully into SQLite database.")
