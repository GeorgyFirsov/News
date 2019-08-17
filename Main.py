import warnings

from os import getcwd, system
from sys import platform

import pandas as pd

import StocksParser.StocksParser as StocksParser
import NewsParser.NewsParser as NewsParser
import Algorythms.Classification as Classification
import Algorythms.Create_features as Features
import Algorythms.Predict as Predictor


#
# Configuration
#

warnings.filterwarnings('ignore')

#
# Debugging
#


DEBUG = 0


def trace(string):
    if DEBUG:
        print('Debugging message: ' + string)


#
# Paths
#


STOCKS_DIR  = getcwd()      # Directory with parsed stocks. Ends with '\' or '/'.
NEWS_DIR    = getcwd()      # Directory with parsed news. Ends with '\' or '/'.
NEWSS_DIR   = getcwd()      # Directory with processed news. Ends with '\' or '/'.
TRAIN_PATH  = getcwd()      # Path to train set.
PICKLE_PATH = getcwd()      # Path to predictor binary file
MAIN_FILE   = 'company.csv' # Path to list of companies.
driver_path = '/Driver/'

# driver_path = '/Driver/chromedriver_Linux' or '/Driver/chromedriver_Windows.exe'
if platform == "win32":
    STOCKS_DIR  += '\\StocksP\\'
    NEWS_DIR    += '\\NewsP\\'
    NEWSS_DIR   += '\\NewssP\\'
    TRAIN_PATH  += '\\Algorythms\\train.csv'
    PICKLE_PATH += '\\Algorythms\\Predictor.pickle'

    driver_path += 'chromedriver_Windows.exe'
else:  # Linux and Mac OS X
    STOCKS_DIR  += '/StocksP/'
    NEWS_DIR    += '/NewsP/'
    NEWSS_DIR   += '/NewssP/'
    TRAIN_PATH  += '/Algorythms/train.csv'
    PICKLE_PATH += '/Algorythms/Predictor.pickle'

    driver_path += 'chromedriver_Linux'

system('mkdir ' + STOCKS_DIR)
system('mkdir ' + NEWS_DIR)
system('mkdir ' + NEWSS_DIR)


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

    StocksParser.main(MAIN_FILE, STOCKS_DIR)
    print('\nОжидание новостей... Это может занять некоторое время\n')
    NewsParser.main(driver_path, MAIN_FILE, NEWS_DIR)
    Classification.main(MAIN_FILE, NEWS_DIR, NEWSS_DIR, TRAIN_PATH)


def prediction_to_string(value):
    if value == 1:
        return 'вырастет'
    else:
        return 'упадёт'


if __name__ == '__main__':
    """Main code of this file
    Performs all the actions of application
    """

    trace('MAIN_FILE  : ' + MAIN_FILE)
    trace('STOCKS_DIR : ' + STOCKS_DIR)
    trace('NEWS_DIR   : ' + NEWS_DIR)
    trace('NEWSS_DIR  : ' + NEWSS_DIR)
    trace('TRAIN_PATH : ' + TRAIN_PATH)

    list_of_companies = pd.read_csv(MAIN_FILE)

    update()

    # Raw working data
    data = Features.main(list_of_companies, NEWSS_DIR, STOCKS_DIR)

    predictions = Predictor.prediction(PICKLE_PATH, data)
    names = list_of_companies.Company.values

    print("\n")

    for name, prediction in zip(names, predictions):
        print("{} - {}".format(name, prediction_to_string(prediction)))

    print("")
