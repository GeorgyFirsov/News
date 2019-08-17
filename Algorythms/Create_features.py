import pandas as pd
from datetime import datetime, timedelta


def create_dataframe(list_of_companies, NEWSS_DIR,STOCKS_DIR):
    tickers = list(list_of_companies.Ticker.values)
    names = list(list_of_companies.Company.values)
    Increase_list = []
    Decrease_list = []
    Positive_number = []
    Negative_number = []
    Change_price = []
    for ticker in tickers:
        df1 = pd.read_csv(NEWSS_DIR +'Newss' + ticker + '.csv', sep = ',', encoding= 'utf-8')
        df1.Date = df1.Date.apply(to_datetime)
        df2 = pd.read_csv(STOCKS_DIR + 'Stocks' + ticker + '.csv', sep = ',', encoding = 'utf-8')
        df2['Date'] = df2['Date'].apply(to_datetime2)
        check_date = datetime.today().date()
        if (datetime.today().weekday() == 6):
            start_date = check_date - timedelta(days = 6)
            end_date = check_date - timedelta(days = 2)
        elif (datetime.today().weekday() == 5):
            start_date = check_date - timedelta(days = 5)
            end_date = check_date - timedelta(days = 1)
        elif (datetime.today().weekday() == 4):
            start_date = check_date - timedelta(days = 7)
            end_date = check_date - timedelta(days = 1)
        elif (datetime.today().weekday() == 3):
            start_date = check_date - timedelta(days = 7)
            end_date = check_date - timedelta(days = 1)
        elif (datetime.today().weekday() == 2):
            start_date = check_date - timedelta(days = 7)
            end_date = check_date - timedelta(days = 1)
        elif (datetime.today().weekday() == 1):
            start_date = check_date - timedelta(days = 7)
            end_date = check_date - timedelta(days = 1)
        elif (datetime.today().weekday() == 0):
            start_date = check_date - timedelta(days = 7)
            end_date = check_date - timedelta(days = 3)
        positive = df1[df1.Date >= start_date][df1.Date <= end_date].label.sum()
        count = df1[df1.Date >= start_date][df1.Date <= end_date].label.count()
        negative = count - positive
        Positive_number.append(positive)
        Negative_number.append(negative)
        max_ = df2[df2['Date'] >= start_date][df2['Date'] <= end_date]['High'].max()
        mean_ = df2[df2['Date'] >= start_date][df2['Date'] <= end_date]['Close'].mean()
        min_ = df2[df2['Date'] >= start_date][df2['Date'] <= end_date]['Low'].min()
        open_ = df2[df2['Date'] == start_date]['Open'].mean()
        close_ = df2[df2['Date'] == end_date]['Close'].mean()
        MAX = max_/mean_
        MIN = min_/mean_
        CHANGE = (close_ - open_)/open_
        Increase_list.append(MAX)
        Decrease_list.append(MIN)
        Change_price.append(CHANGE)

    df = pd.DataFrame({'Company':names, 'Max_Increase': Increase_list, 'Max_Decrease': Decrease_list, 'Positive_number': Positive_number, 'Negative_number': Negative_number, 'Change_prise': Change_price})
    return df

def to_datetime(string_):
    date = datetime.strptime(string_,"%d.%m.%Y")
    return date.date()

def to_datetime2(number):
    year = int(number / 10000)
    year +=2000
    month = int((number / 100) % 100)
    day = number % 100
    date = datetime(year,month,day)
    return date.date()

def main(list_of_companies, NEWSS_DIR,STOCKS_DIR):
    return create_dataframe(list_of_companies, NEWSS_DIR, STOCKS_DIR)

