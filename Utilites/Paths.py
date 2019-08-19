# This file contains necessary paths
from os import getcwd
from sys import platform

stocks_directory = getcwd() + '/data/StocksP/'          # Directory with parsed stocks. Ends with '/'.
news_directory   = getcwd() + '/data/NewsP/'            # Directory with parsed news. Ends with '/'.
prnews_directory = getcwd() + '/data/NewssP/'           # Directory with processed news. Ends with '/'.
train_set_path   = getcwd() + '/data/train.csv'         # Path to train set.
binary_path      = getcwd() + '/data/Predictor.pickle'  # Path to predictor binary file
companies_file   = getcwd() + '/data/company.csv'       # Path to list of companies.
driver_path      = getcwd() + '/Driver/'                # Path to Chrome driver

driver_path += 'chromedriver_Windows.exe' if platform == 'win32' else 'chromedriver_Linux'
