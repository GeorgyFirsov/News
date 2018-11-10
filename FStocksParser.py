from datetime import datetime
import fix_yahoo_finance as yf

tickers = ['AAPL', 'GOOG', 'GOOGL', 'MSFT']
start = datetime(2018,5,31)
end = datetime(2018,11,11)

for ticker in tickers:
    data = yf.download(ticker, start = start, end = end)
    data.sort_values(by = ['Date'], ascending = False, inplace = True)
    print(ticker, "\n", data.head())
    fname = 'STOCKS_'
    fname += ticker
    fname += '.csv'
    data.to_csv(path_or_buf = fname, sep = ',')