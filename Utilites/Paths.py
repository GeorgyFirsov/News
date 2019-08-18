# This file contains necessary paths

from os import getcwd
from sys import platform

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