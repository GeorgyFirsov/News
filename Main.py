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
import datetime
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
import Algorythms.stocks_check as stocksch
from threading import Thread
from time import sleep

########################################################################
########################### Константы ##################################
########################################################################

MAIN_FILE = 'company.csv'
STOCKS_DIR = getcwd()
NEWS_DIR = getcwd()
DATE_START = 0
DATE_CLOSE = 0

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
    print('MAIN_FILE  : ' + MAIN_FILE)
    print('STOCKS_DIR : ' + STOCKS_DIR)
    print('NEWS_DIR   : ' + NEWS_DIR)
    thread1 = Thread(target = stocksp.main_, args = (MAIN_FILE, STOCKS_DIR, ))
    thread2 = Thread(target = newsp.main_, args = (MAIN_FILE, NEWS_DIR, ))
    list_of_companies = pd.read_csv(MAIN_FILE)
    thread1.start()
    thread2.start()
    thread1.join()
    print('\nWaiting for news... It may take a while\n')
    thread2.join()
    DATE_START = datetime.datetime.today() - datetime.timedelta(days = 1)
    DATE_CLOSE = datetime.datetime(2018, 11, 23)
    for row in list_of_companies.itertuples():
        print(row[2] + ' change: ' + str(stocksch.main_(STOCKS_DIR, str(row[2]), DATE_START, DATE_CLOSE)))

if __name__ == '__main__':
     main()
