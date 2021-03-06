# This file contains creator of data frame for predictor
from datetime import datetime, timedelta

import pandas as pd


class FeaturesCreator:
    """Provides creation of data frame with features that will be forwarded
    to the predictor. Receives data frame with list of companies and paths
    to directories with classified news and stocks

    Fields:
        __tickers: list of tickers
        __names: list of names of companies
        __clnews_directory: path to directory with classified news
        __stocks_directory: path to directory with parsed stocks
    """

    def __init__(self, list_of_companies, clnews_directory: str, stocks_directory: str):
        self.__tickers = list(list_of_companies.Ticker.values)
        self.__names   = list(list_of_companies.Company.values)
        self.__clnews_directory = clnews_directory
        self.__stocks_directory = stocks_directory

    def create(self):
        """Converts classified news and stocks into data frame with features
        that will be forwarded to predictor.

        :return: data frame ready to pass to predictor
        """

        increase_list   = list()
        decrease_list   = list()
        positive_number = list()
        negative_number = list()
        change_price    = list()

        for ticker in self.__tickers:
            data_frame_news = pd.read_csv(self.__clnews_directory + 'Newss' + ticker + '.csv'
                                          , encoding='utf-8', sep=',')
            data_frame_news.Date = data_frame_news.Date.apply(to_datetime_n)

            data_frame_stocks = pd.read_csv(self.__stocks_directory + 'Stocks' + ticker + '.csv'
                                            , encoding='utf-8', sep=',')
            data_frame_stocks['Date'] = data_frame_stocks['Date'].apply(to_datetime_st)

            deltas = {
                0: (7, 3), 1: (7, 1), 2: (7, 1), 3: (7, 1),
                4: (7, 1), 5: (5, 1), 6: (6, 2)
            }

            check_date = datetime.today().date()
            today_week_day = datetime.today().weekday()

            start_date = check_date - timedelta(days=deltas[today_week_day][0])
            end_date   = check_date - timedelta(days=deltas[today_week_day][1])

            positive = data_frame_news[data_frame_news.Date >= start_date][data_frame_news.Date <= end_date].label.sum()
            count    = data_frame_news[data_frame_news.Date >= start_date][data_frame_news.Date <= end_date].label.count()

            positive_number.append(positive)
            negative_number.append(count - positive)

            max_of_high   = data_frame_stocks[data_frame_stocks['Date'] >= start_date][data_frame_stocks['Date'] <= end_date]['High'].max()
            mean_on_close = data_frame_stocks[data_frame_stocks['Date'] >= start_date][data_frame_stocks['Date'] <= end_date]['Close'].mean()
            min_of_low    = data_frame_stocks[data_frame_stocks['Date'] >= start_date][data_frame_stocks['Date'] <= end_date]['Low'].min()
            mean_on_close_first = data_frame_stocks[data_frame_stocks['Date'] == start_date]['Open'].mean()
            mean_on_close_last  = data_frame_stocks[data_frame_stocks['Date'] == end_date]['Close'].mean()

            max_moderate = max_of_high / mean_on_close
            min_moderate = min_of_low / mean_on_close
            change = (mean_on_close_last - mean_on_close_first) / mean_on_close_first

            increase_list.append(max_moderate)
            decrease_list.append(min_moderate)
            change_price.append(change)

        data_frame = pd.DataFrame({'Company': self.__names, 'Max_Increase': increase_list
                                  , 'Max_Decrease': decrease_list, 'positive_number': positive_number
                                  , 'negative_number': negative_number, 'Change_prise': change_price})

        return data_frame

# End of FeaturesCreator class ---------------------------------------------


def to_datetime_n(date_as_string: str):
    """Converts date from news to specified format
    """

    date = datetime.strptime(date_as_string, "%d.%m.%Y")
    return date.date()


def to_datetime_st(time_as_number: int):
    """Converts date from stocks to specified format
    """

    year = int(time_as_number / 10000) + 2000
    month = int((time_as_number / 100) % 100)
    day = time_as_number % 100
    return datetime(year, month, day).date()


def create(list_of_companies, clnews_directory: str, stocks_directory: str):
    """Performs main function of this module - converts
    parsed data to predictor-friendly data frame.

    :param list_of_companies: data frame with list of companies
    :param clnews_directory: path to directory with classified news
    :param stocks_directory: path to directory with parsed stocks

    :return: data frame with features
    """

    creator = FeaturesCreator(list_of_companies, clnews_directory, stocks_directory)
    return creator.create()

