#
#   Usage:
#
#       To get access to functions from News Parser type:
#           newsp.%function%
#
#       To get access to functions from Stocks Parser type:
#           stocksp.%function%
#

import pandas as pd
from os import getcwd
from sys import platform
from sys import path
if platform == "linux" or platform == "linux2":
    path.insert(0, getcwd() + '/NewsParser/Linux')
elif platform == "win32":
    path.insert(0, getcwd() + '/NewsParser/Windows')
import StocksParser.StocksParser as stocksp
import NewsParser as newsp

def main():
    list_of_companies = pd.read_csv('company.csv')
    print(list_of_companies)

if __name__ == '__main__':
     main()