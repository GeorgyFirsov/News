from time import sleep

import pandas as pd
from datetime import datetime, timedelta


def make_url(market_, em_, code_, df_, mf_, yf_
             , from_, dt_, mt_, yt_, to_, f_, p_
             , e_, cn_, dtf_, tmf_, MSOR_, mstime_
             , mstimever_):
    """This function composes request url from
    passed arguments. This url will return a
    *.csv file from www.finam.ru.

    Argument's names are even with corresponding
    url variable.
    """

    url = "http://export.finam.ru/" + f_ + ".csv?"
    url += "market=" + str(market_) + "?&em="    + str(em_)
    url += "&code="  + str(code_)   + "&apply="  + str(0)
    url += "&df="    + str(df_)     + "&mf="     + str(mf_)
    url += "&yf="    + str(yf_)     + "&from="   + str(from_)
    url += "&dt="    + str(dt_)     + "&mt="     + str(mt_)
    url += "&yt="    + str(yt_)     + "&to="     + str(to_)
    url += "&p="     + str(p_)      + "&f="      + str(f_)
    url += "&e="     + str(e_)      + "&cn="     + str(cn_)
    url += "&dtf="   + str(dtf_)    + "&tmf="    + str(tmf_)
    url += "&MSOR="  + str(MSOR_)   + "&mstime=" + str(mstime_)
    url += "&mstimever=" + str(mstimever_)
    url += "&sep=1&sep2=1&datf=1&at=1"
    return url


def processing(path_, row, market, day_from, month_from, year_from
               , start_date, day_to, month_to, year_to, end_date):
    """Receives two dates and ticker, makes request
    to www.finam.ru and saves parsed information
    to *.csv file to file path_.
    """

    # day time delay
    hours_delta = 8

    today = datetime.today()
    now   = datetime.now()

    fn = row[1] + str(today.day)  + str(today.month) + str(today.year) \
                + str(now.second) + str(now.minute)  + str(now.hour)

    url = make_url(market, row[2], row[1], day_from, month_from, year_from
                   , start_date, day_to, month_to, year_to, end_date, fn
                   , hours_delta, '.csv', row[1], 2, 1, 1, 'on', 1)

    sleep(0.8)

    data = pd.read_csv(url)

    data = data.drop(data.columns[[1, 3]], axis=1)
    data.columns = ['' + title for title in ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    file_name = path_ + 'Stocks' + row[1] + ".csv"
    data.to_csv(file_name)

    print(row[1] + ' - готово')


def get_dataframe(file_name, path_):
    """Receives file with list of companies and
    directory path, where dataframes should
    be saved.
    Puts parsed dataframes to this folder.
    """

    if file_name is None:
        raise Exception('File name can not be empty')
    if path_ is None:
        raise Exception('Empty path')

    # starting date is days_delta days ago
    days_delta = 7

    today = datetime.today()
    start_day = (today - timedelta(days=days_delta)).date()

    start_date = str(start_day.day) + '.' \
               + str(start_day.month) + '.' \
               + str(start_day.year)
    end_date   = str(today.day) + '.' \
               + str(today.month) + '.' \
               + str(today.year)

    day_from   = start_day.day
    month_from = start_day.month - 1
    year_from  = start_day.year
    day_to     = today.day
    month_to   = today.month - 1
    year_to    = today.year

    market = 1

    data = pd.read_csv(file_name).drop('Company', axis=1)

    for row in data.itertuples():
        processing(path_, row, market, day_from, month_from, year_from
                   , start_date, day_to, month_to, year_to, end_date)


def main_(file_name=None, path_=None):
    get_dataframe(file_name, path_)
