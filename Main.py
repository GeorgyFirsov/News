import warnings
from os import getcwd, system
from sys import platform

import pandas as pd

import StocksParser.StocksParser as StocksParser
import NewsParser.NewsParser as NewsParser
import Algorithms.Classification as Classification
import Algorithms.CreateFeatures as Features
import Algorithms.Predict as Predictor
from Trace.Trace import trace


#
# Configuration
#

warnings.filterwarnings('ignore')
debug = False

#
# Paths
#


stocks_directory = getcwd()       # Directory with parsed stocks. Ends with '\' or '/'.
news_directory   = getcwd()       # Directory with parsed news. Ends with '\' or '/'.
prnews_directory = getcwd()       # Directory with processed news. Ends with '\' or '/'.
train_set_path   = getcwd()       # Path to train set.
binary_path      = getcwd()       # Path to predictor binary file
companies_file   = 'company.csv'  # Path to list of companies.
driver_path      = '/Driver/'     # Relative path to predictor binary

if platform == "win32":
    stocks_directory  += '\\StocksP\\'
    news_directory    += '\\NewsP\\'
    prnews_directory  += '\\NewssP\\'
    train_set_path    += '\\Algorithms\\train.csv'
    binary_path       += '\\Algorithms\\Predictor.pickle'
    driver_path       += 'chromedriver_Windows.exe'
else:  # Linux and Mac OS X
    stocks_directory  += '/StocksP/'
    news_directory    += '/NewsP/'
    prnews_directory  += '/NewssP/'
    train_set_path    += '/Algorithms/train.csv'
    binary_path       += '/Algorithms/Predictor.pickle'
    driver_path       += 'chromedriver_Linux'

system('mkdir ' + stocks_directory)
system('mkdir ' + news_directory)
system('mkdir ' + prnews_directory)


#
# Implementation
#


def update():
    """This function asks user if he or
    she wants to update data to the newest.
    If the answer is 'yes' performs update
    """

    print('\n\nОбновить данные?')
    print('\t1 - да\n\t2 - нет')

    answer = 0
    while answer != 1 and answer != 2:
        print(' > ', end='')

        try:
            answer = int(input())
        except ValueError:
            continue

    if answer == 2:
        return

    print("\n", end='')

    StocksParser.main(companies_file, stocks_directory)
    print('\nОжидание новостей... Это может занять некоторое время\n')
    NewsParser.main(driver_path, companies_file, news_directory)
    Classification.main(companies_file, news_directory, prnews_directory, train_set_path)


def prediction_to_string(value):
    return 'вырастет' if value else 'упадёт'


if __name__ == '__main__':
    """Main code of this file
    Performs all the actions of application
    """

    trace('companies_file   : ' + companies_file, debug)
    trace('stocks_directory : ' + stocks_directory, debug)
    trace('news_directory   : ' + news_directory, debug)
    trace('prnews_directory : ' + prnews_directory, debug)
    trace('train_set_path   : ' + train_set_path, debug)
    trace('driver_path      : ' + driver_path, debug)

    list_of_companies = pd.read_csv(companies_file)

    update()

    # Raw working data
    data = Features.create(list_of_companies, prnews_directory, stocks_directory)

    predictions = Predictor.prediction(binary_path, data)
    names = list_of_companies.Company.values

    print("\n")

    for name, prediction in zip(names, predictions):
        print("{} - {}".format(name, prediction_to_string(prediction)))

    print("")
