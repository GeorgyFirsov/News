#
#   Использование:
#
#       Доступ к функциям парсера новостей:
#           newsp.%function%
#
#       Доступ к функциям парсера акций:
#           stocksp.%function%
#
#   MAIN_FILE  - файл со списком компаний. Должен лежать рядом с исполняемым файлом
#
#   STOCKS_DIR - директория со спарсенными акциями. Оканчивается на \ или /
#
#   NEWS_DIR   - директория со спарсенными новостями. Оканчивается на \ или /
#

import pandas as pd
from os import getcwd
from os import system
from sys import platform
from sys import path
if platform == "linux" or platform == "linux2":
    path.insert(0, getcwd() + '/NewsParser/Linux')
elif platform == "win32":
    path.insert(0, getcwd() + '/NewsParser/Windows')
import StocksParser.StocksParser as stocksp
import NewsParser as newsp

########################################################################
########################### Константы ##################################
########################################################################

MAIN_FILE = 'company.csv'
STOCKS_DIR = getcwd()
NEWS_DIR = getcwd()

########################################################################
########################## Конфигурация ################################
########################################################################

if platform == "linux" or platform == "linux2":
    STOCKS_DIR += '/StocksP/'
    NEWS_DIR += '/NewsP/'
elif platform == "win32":
    STOCKS_DIR += '\\StocksP\\'
    NEWS_DIR += '\\NewsP\\'

createSD = 'mkdir ' + STOCKS_DIR
createND = 'mkdir ' + NEWS_DIR

system(createSD)
system(createND)

del createSD
del createND

########################################################################
##################### Окончание конфигурации ###########################
########################################################################

def main():
    list_of_companies = pd.read_csv(MAIN_FILE)
    stocksp.main(MAIN_FILE, STOCKS_DIR)
    newsp.main(MAIN_FILE, NEWS_DIR)

if __name__ == '__main__':
     main()