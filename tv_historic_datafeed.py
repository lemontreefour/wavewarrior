# Import necessary libraries
# pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git --break-system-packages
from tvDatafeed import TvDatafeed, Interval
import sqlite3
import argparse

# Initialize TvDatafeed without authentication
tv = TvDatafeed()

intervals = dict(
	# Available intervals for historical data
	min_1 = Interval.in_1_minute,
	min_2 = Interval.in_3_minute,
	min_5 = Interval.in_5_minute,
	min_15 = Interval.in_15_minute,
	min_30 = Interval.in_30_minute,
	min_45 = Interval.in_45_minute,
	hour_1 = Interval.in_1_hour,
	hour_2 = Interval.in_2_hour,
	hour_3 = Interval.in_3_hour,
	hour_4 = Interval.in_4_hour,
	daily = Interval.in_daily,
	weekly = Interval.in_weekly,
	monthly = Interval.in_monthly
)

# Create an argument parser
parser = argparse.ArgumentParser(description='Fetch historical stock data and store it in a SQLite database.')
# Add arguments for symbol, exchange, and bars
parser.add_argument('--symbol', type=str, default='PATEK', help='Stock symbol (default: PATEK)')
parser.add_argument('--exchange', type=str, default='BIST', help='Exchange name (default: BIST)')
parser.add_argument('--interval', type=str, default='hour_1', help='Data interval (default: one hour)')
parser.add_argument('--bars', type=int, default=1000, help='Number of historical bars to fetch (default: 1000)')
# Parse the arguments
args = parser.parse_args()

# Set the variables from the parsed arguments
symbol_name = args.symbol
exchange_source = args.exchange
data_interval = args.interval
bars_history = args.bars

# Fetch historical data from TradingView
stock_data = tv.get_hist(symbol = symbol_name, exchange = exchange_source, interval = intervals.get(data_interval), n_bars = bars_history)

print(f'Retrieving {bars_history} data for {symbol_name} from TradingView which is listed in {exchange_source} exchange with data interval of {data_interval} and saving to {symbol_name}.db sqlite database.')

# -- Store data in sqlite database --
# Define the name of the database file
db_file = f"{symbol_name}.db"
# Connect to the SQLite database
conn = sqlite3.connect(db_file)
# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create a table to store stock data if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        DateTime TEXT UNIQUE,
        Symbol TEXT,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Volume REAL
    )
''')

# Iterate over the fetched stock data and insert it into the database
for index, row in stock_data.iterrows():
    # Execute the INSERT OR IGNORE command to add a new row to the table
    c.execute('''
        INSERT OR IGNORE INTO stock_data (DateTime, Symbol, Open, High, Low, Close, Volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        # Format the datetime to a string
        index.strftime('%Y-%m-%d %H:%M:%S'),
        # Create the symbol string
        f"{exchange_source}:{symbol_name}",
        # Get the open price
        row['open'],
        # Get the high price
        row['high'],
        # Get the low price
        row['low'],
        # Get the close price
        row['close'],
        # Get the volume
        row['volume']
    ))

# Commit the changes to the database
conn.commit()
# Close the database connection
conn.close()

# Print a confirmation message
print(f"Data for {symbol_name} stored in {db_file}")