# Stock Screener ETL

#### **Video Demo:** <https://youtu.be/mDRdTjSaiMM>

#### **Description:**

Extract, Transform, Load or more commonly known as ETL, is one of the most popular and used techniques in the data engineering field.
This program performs a whole ETL process from start to finish, ultimately creating a stock screener database file which can be SQL queried. Not only that, but it adds an extra twist by making the program interactive.

The purpose is to extract financial data from YahooFinance and create a stock screener. The user is prompted what type of stock screener would he/she like to receive: Top Daily Winners, Top Daily Losers, or Most Active Stocks. Once the user provides his/her preference, the program uses real time data, to extract all company tickers, their corresponding financial attributes and create a data frame. The generated data frame is then cleaned via a transformation process and finally loaded to a database file, which is named depending on the type of screener selected by the user.

#### **Requirements**

To have this program up and running, a few libraries are needed to be installed and imported to the file. A list of the used libraries can be found in [``requirements.txt``](/workspaces/155151931/project/requirements.txt).

#### **Functions**

``main():``

The main() function combines 4 functions, executing each one after the other, as the output of each function is then used as an input for the following function.

``user_decision():``

The user_decision() function starts the program by prompting the user for a selection. 4 choices are avaiable - Daily Stock Gainers, Daily Stock Losers, Most Active Stocks,  and exit the program. Any invalid inputs such as non-integers and integers which are != [1,2,3] are caught using a try-except statement. Appropriate error messages are raised.
If the option is 0, the program exits via sys.Exit with an appropriate exit message.
If the input is 1,2 or 3, the program returns the particular choice, as well as, the link attached to the corresponding number (each option has a specific link attached to it).

``extract():``

The extract() function takes the link from the previous function and reads it as an HTML file. Then it proceeds to take all of the tickers from the HTML and put them in a list. A list comprehension is then used to return certain financial attributes for each of the tickers in the list with the help of yfinance module. Finally, this creates a key-value pair dictionary which is converted to a DataFrame.

``transform():``

The transform() function takes the newly-created DataFrame from the previous function and executes a couple of clean up techniques such as converting large values to Billions/Millions, rounding to second decimal, column renaming and setting the starting index to 1. This returns a cleaned DataFrame.

``load():``

The load() function takes the cleaned DataFrame, as well as, the user input from the user_decision() function. A database file is created and by using an IF statement, depending on the user decision, the database file is named accordingly. Then an sqlite3 connection is created. We load the cleaned DataFrame to the newly created database file, save it and finally close the connection.

#### **Final output**

Once the data is extracted, transformed and loaded to a database, a database file will be created in the project's directory. To be able to see the contents of the file, there are two options:

1. Install the SQLite Viewer extension and open the file directly in VScode using the extension.
2. Go to an online SQLite Viewer such as https://inloop.github.io/sqlite-viewer/ and drop the file.

#### **Testing**

The program has been tested using Pytest in a dedicated file [``test_project.py``](/workspaces/155151931/project/test_project.py). A test function has been implemented for each of the functions in ``project.py``. Each of the tests assert correctness of the functions and all 4 tests pass successfully.
