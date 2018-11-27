import pandas as pd
import datetime

def check_stock(path_,stock,date_start,date_close):
    boof1 = 0 # храним конец торгов(значение) для 1 даты
    boof2 = 0 # храним конец торгов(значение) для 2 даты
    boof = 0  # флажочек))0)
    date_start = convert_date(date_start)
    date_close = convert_date(date_close)
    name_file = path_ + "Stocks" + stock + ".csv"
    file = pd.read_csv(name_file)
    for row in file.itertuples():
        if(int(row[3]) >= date_start) and (boof == 0):
            boof1=float(row[7])
            boof+=1
        if(int(row[3]) <= date_close):
            boof2=float(row[7])
        if(int(row[3]) >= date_close) and (boof == 1):
            if(boof1 == boof2):
                return 0
            if(boof1 < boof2):
                return 1
            if(boof1 > boof2):
                return -1
    return(-2)

def convert_date(date):
    date_new = (int(date.year) - 2000) * 10000 + int(date.month) * 100 + int(date.day)
    return date_new

def main_(path_, stock, start, close):
    check_stock(path_, stock, start, close)