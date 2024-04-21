# Import needed libraries
import pandas as pd
import yfinance as yf
import sqlite3
import sys

# Main ETL: get user's stock report preference, extract, transform, load and name the db file appropriately.
def main():
    link, selection = user_decision()
    extracted_data = extract(link)
    transformed_data = transform(extracted_data)
    load(transformed_data, selection)

# Promt user for stock report selection. Catch any errors and return the link corresponding to the user selection.
def user_decision():
    print("Welcome to the stock screener ETL. What report would you like to get?\n")
    print("For Daily Gainers - select 1\nFor Daily Losers - select 2\nFor Most Active - select 3\nTo exit - select 0\n")
    while True:
        selection = input("Which option do you select? ")
        try:
            selection = int(selection)
        except ValueError:
            print("Invalid input. Please enter a numeric option.")
            continue

        if selection in [1,2,3]:
            if selection == 1:
                link = "https://finance.yahoo.com/screener/predefined/day_gainers?count=100&offset=0"
            elif selection == 2:
                link = "https://finance.yahoo.com/screener/predefined/day_losers?offset=0&count=100"
            elif selection == 3:
                link = "https://finance.yahoo.com/screener/predefined/most_actives?offset=0&count=100"
            return link, selection
        elif selection == 0:
            sys.exit("Goodbye")
        else:
            print("Please use the avaiable options.")

# Extract function: extract tickers from the provided link and their corresponding attributes. Create a DataFrame.
def extract(link):
    print("Starting data extraction...")
    HTML_data = pd.read_html(link)[0]
    ticker_list = HTML_data["Symbol"].to_list()
    stock_data = [
        {
            "Ticker":ticker,
            "Name" : yf.Ticker(ticker).info.get("longName"),
            "Country" : yf.Ticker(ticker).info.get("country"),
            "Industry" : yf.Ticker(ticker).info.get("industry"),
            "Market Cap" : yf.Ticker(ticker).info.get("marketCap"),
            "Volume" : yf.Ticker(ticker).info.get("averageVolume"),
            "Price" : yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1],
            "Currency" : yf.Ticker(ticker).info.get("currency")
        }
        for ticker in ticker_list
    ]
    df = pd.DataFrame(stock_data)
    print("Data extracted.")
    return df

# Transform function: Clean the DataFrame
def transform(data):
    data["Market Cap"] = round(data["Market Cap"] / 1000000000, 2)
    data["Volume"] = round(data["Volume"] / 1000000, 2)
    data.rename(columns={"Market Cap" : "Market Cap (Billions)", "Volume" : "Volume (Millions)"}, inplace = True)
    data["Price"] = round(data["Price"], 2)
    data.index += 1
    print("Data transformed.")
    return data

# Load function: Create a database and save the cleaned data. Name the file appropriately.
def load(clean_data, file_name):
    if file_name == 1:
        db_name = "daily_stock_gainers.db"
    elif file_name == 2:
        db_name = "daily_stock_losers.db"
    else:
        db_name = "most_active_stocks.db"
    conn = sqlite3.connect(db_name)
    clean_data.to_sql(db_name, conn, if_exists = "replace")
    conn.close()
    print("Data loaded to database.")

# Execute main
if __name__ == "__main__":
    main()
