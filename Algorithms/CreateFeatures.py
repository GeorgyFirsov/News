from datetime import datetime, timedelta

import pandas as pd


def to_datetime_n(date_as_string):
    """Converts date from news to specified format
    """

    date = datetime.strptime(date_as_string, "%d.%m.%Y")
    return date.date()


def to_datetime_st(time_as_number):
    """Converts date from stocks to specified format
    """

    year = int(time_as_number / 10000) + 2000
    month = int((time_as_number / 100) % 100)
    day = time_as_number % 100
    return datetime(year, month, day).date()


class FeaturesCreator:
    """Provides creation of data frame with features that will be forwarded
    to the predictor. Receives data frame with list of companies and paths
    to directories with classified news and stocks

    Fields:
        tickers: list of tickers
        names: list of names of companies
        clnews_directory: path to directory with classified news
        stocks_directory: path to directory with parsed stocks
    """

    def __init__(self, list_of_companies, clnews_directory, stocks_directory):
        self.tickers = list(list_of_companies.Ticker.values)
        self.names   = list(list_of_companies.Company.values)
        self.clnews_directory = clnews_directory
        self.stocks_directory = stocks_directory

    def create(self):
        """Converts classified news and stocks into data frame with features
        that will be forwarded to predictor.

        :return: data frame ready to pass to predictor
        """

        increase_list = list()
        decrease_list = list()
        positive_number = list()
        negative_number = list()
        change_price = list()

        for ticker in self.tickers:
            df1 = pd.read_csv(self.clnews_directory + 'Newss' + ticker + '.csv', sep=',', encoding='utf-8')
            df1.Date = df1.Date.apply(to_datetime_n)

            df2 = pd.read_csv(self.stocks_directory + 'Stocks' + ticker + '.csv', sep=',', encoding='utf-8')
            df2['Date'] = df2['Date'].apply(to_datetime_st)

            deltas = {
                0: (7, 3), 1: (7, 1), 2: (7, 1), 3: (7, 1),
                4: (7, 1), 5: (5, 1), 6: (6, 2)
            }

            check_date = datetime.today().date()
            today_week_day = datetime.today().weekday()

            start_date = check_date - timedelta(days=deltas[today_week_day][0])
            end_date = check_date - timedelta(days=deltas[today_week_day][1])

            positive = df1[df1.Date >= start_date][df1.Date <= end_date].label.sum()
            count = df1[df1.Date >= start_date][df1.Date <= end_date].label.count()

            positive_number.append(positive)
            negative_number.append(count - positive)

            max_of_high = df2[df2['Date'] >= start_date][df2['Date'] <= end_date]['High'].max()
            mean_on_close = df2[df2['Date'] >= start_date][df2['Date'] <= end_date]['Close'].mean()
            min_of_low = df2[df2['Date'] >= start_date][df2['Date'] <= end_date]['Low'].min()
            mean_on_close_first = df2[df2['Date'] == start_date]['Open'].mean()
            mean_on_close_last = df2[df2['Date'] == end_date]['Close'].mean()

            max_moderate = max_of_high / mean_on_close
            min_moderate = min_of_low / mean_on_close
            change = (mean_on_close_last - mean_on_close_first) / mean_on_close_first

            increase_list.append(max_moderate)
            decrease_list.append(min_moderate)
            change_price.append(change)

        data_frame = pd.DataFrame({'Company': self.names, 'Max_Increase': increase_list
                                  , 'Max_Decrease': decrease_list, 'positive_number': positive_number
                                  , 'negative_number': negative_number, 'Change_prise': change_price})

        return data_frame


def create(list_of_companies, clnews_directory, stocks_directory):
    """Performs main function of this module - converts
    parsed data to predictor-friendly data frame

    :param list_of_companies: data frame with list of companies
    :param clnews_directory: path to directory with classified news
    :param stocks_directory: path to directory with parsed stocks

    :return: data frame with features
    """

    creator = FeaturesCreator(list_of_companies, clnews_directory, stocks_directory)
    return creator.create()

