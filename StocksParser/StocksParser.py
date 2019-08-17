from time import sleep

import pandas as pd
from datetime import datetime, timedelta


class StocksParser:
    """This class provides stocks parsing from site

    Fields:
        __file_name: file with list of companies
        __store_path: path to directory where stocks will be saved
    """

    def __init__(self, file_name, store_path):
        """Constructs parser object.
        It checks if all field are not empty
        and if not, throws an exception.
        """

        if file_name is None \
                or store_path is None:
            raise Exception("All paths must be specified")

        self.__file_name  = file_name
        self.__store_path = store_path

    def parse_stocks(self):
        """Receives file with list of companies and
        directory path, where data frames should
        be saved.
        Puts parsed data frames to this folder.
        """

        # starting date is days_delta days ago
        days_delta = 7

        today = datetime.today()
        start_day = (today - timedelta(days=days_delta)).date()

        start_date = str(start_day.day) + '.' \
                     + str(start_day.month) + '.' \
                     + str(start_day.year)
        end_date = str(today.day) + '.' \
                   + str(today.month) + '.' \
                   + str(today.year)

        day_from   = start_day.day
        month_from = start_day.month - 1
        year_from  = start_day.year
        day_to     = today.day
        month_to   = today.month - 1
        year_to    = today.year

        market = 1

        data = pd.read_csv(self.__file_name).drop('Company', axis=1)

        for row in data.itertuples():
            processing(self.__store_path, row, market, day_from, month_from, year_from
                       , start_date, day_to, month_to, year_to, end_date)

# End of StocksParser class ------------------------------------------------


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


def processing(store_path, row, market, day_from, month_from, year_from
               , start_date, day_to, month_to, year_to, end_date):
    """Receives two dates and ticker, makes request
    to www.finam.ru and saves parsed information
    to *.csv file to file path_.

    :param store_path: full path to folder to store with data
    :param row: item in list of companies (line in file)
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

    # Wait some time not to be banned
    # 0.8 sec - shortest experimentally
    # proved delay
    sleep(0.8)

    data = pd.read_csv(url)

    data = data.drop(data.columns[[1, 3]], axis=1)
    data.columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    store_path = store_path + 'Stocks' + row[1] + ".csv"
    data.to_csv(store_path)

    print(row[1] + ' - готово')


def parse(file_name=None, path=None):
    """Main entry point of module. Called from Main.py.

    :param file_name: file with list of companies
    :param path: path to directory where stocks will be saved
    """

    parser = StocksParser(file_name, path)
    parser.parse_stocks()
