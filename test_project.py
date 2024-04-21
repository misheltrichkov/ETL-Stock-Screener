# Import needed modules
from project import user_decision, extract, transform, load
import pytest
import sys
import pandas as pd

# Test user decision. To simulate user's input we use a mock input and validate if the function reacts as espected.
def test_user_decision(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda input: 0)
    with pytest.raises(SystemExit) as e:
        user_decision()
    assert e.type == SystemExit
    assert e.value.code == "Goodbye"

# Test extraction phase. Validate if a DataFrame is created and whether the columns are as expected.
def test_extract():
    link = "https://finance.yahoo.com/screener/predefined/day_gainers?count=100&offset=0"
    df = extract(link)
    assert isinstance(df, pd.DataFrame)
    expected_columns = ["Ticker", "Name" , "Country" ,"Industry","Market Cap" ,"Volume","Price","Currency"]
    assert df.columns.to_list() == expected_columns

# Test transformation phase. Validate if columns are renamed as expected.
def test_transform():
    link = "https://finance.yahoo.com/screener/predefined/day_gainers?count=100&offset=0"
    df = extract(link)
    df2 = transform(df)
    expected_columns = ["Ticker", "Name" , "Country" ,"Industry","Market Cap (Billions)" ,"Volume (Millions)","Price","Currency"]
    assert df2.columns.to_list() == expected_columns

# Test load phase. Validate if the created database file is named properly.
def test_load():
    link = "https://finance.yahoo.com/screener/predefined/day_gainers?count=100&offset=0"
    df = extract(link)
    df2 = transform(df)
    if load(df2, 1):
        assert db_name == "daily_stock_gainers.db"
    if load(df2, 2):
        assert db_name == "daily_stock_losers.db"
    if load(df2, 3):
        assert db_name == "most_active_stocks.db"
