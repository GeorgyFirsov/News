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

DEBUG = 0

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
import Algorythms.Classification as classify
import Algorythms.Create_features as features
import Algorythms.Predict as predictor
from threading import Thread
from time import sleep
import warnings
warnings.filterwarnings('ignore')

########################################################################
########################### Константы ##################################
########################################################################

MAIN_FILE = 'company.csv'
STOCKS_DIR = getcwd()
NEWS_DIR = getcwd()
NEWSS_DIR = getcwd()
TRAIN_PATH = getcwd()
PICKLE_PATH = getcwd()
DATE_START = 0
DATE_CLOSE = 0

########################################################################
########################## Конфигурация ################################
########################################################################

if platform == "linux" or platform == "linux2":
    STOCKS_DIR += '/StocksP/'
    NEWS_DIR += '/NewsP/'
    NEWSS_DIR += '/NewssP/'
    TRAIN_PATH += '/Algorythms/train.csv'
    PICKLE_PATH += '/Algorythms/Predictor.pickle'
elif platform == "win32":
    STOCKS_DIR += '\\StocksP\\'
    NEWS_DIR += '\\NewsP\\'
    NEWSS_DIR += '\\NewssP\\'
    TRAIN_PATH += '\\Algorythms\\train.csv'
    PICKLE_PATH += '\\Algorythms\\Predictor.pickle'

createSD = 'mkdir ' + STOCKS_DIR
createND = 'mkdir ' + NEWS_DIR
createNSD = 'mkdir ' + NEWSS_DIR

system(createSD)
system(createND)
system(createNSD)

del createSD
del createND
del createNSD

########################################################################
##################### Окончание конфигурации ###########################
########################################################################

def update(parameter):
    if parameter == '2':
        return ' '
    if parameter != '1':
        return 'Allowed answers: 1 or 2'
    thread1 = Thread(target = stocksp.main_, args = (MAIN_FILE, STOCKS_DIR, ))
    thread2 = Thread(target = newsp.main_, args = (MAIN_FILE, NEWS_DIR, ))
    thread1.start()
    thread2.start()
    thread1.join()
    print('\nWaiting for news... It may take a while\n')
    thread2.join()
    classify.main_(MAIN_FILE, NEWS_DIR, NEWSS_DIR, TRAIN_PATH)
    return 'Updated'

def main():
    if DEBUG == 1:
        print('MAIN_FILE  : ' + MAIN_FILE)
        print('STOCKS_DIR : ' + STOCKS_DIR)
        print('NEWS_DIR   : ' + NEWS_DIR)
        print('NEWSS_DIR  : ' + NEWSS_DIR)
        print('TRAIN_PATH : ' + TRAIN_PATH)
    else:
        pass
    list_of_companies = pd.read_csv(MAIN_FILE)
    print('\n\nWould you like to update these files?')
    while True:
        print('\n\n    1 - yes\n    2 - no\n\nYour answer: ', end = '')
        answer = input()
        try:
            answer = int(answer)
            if answer != 1 and answer != 2:
                continue
            break
        except:
            continue
    update(answer)
    DATE_START = datetime.datetime.today() - datetime.timedelta(days = 1)
    DATE_CLOSE = datetime.datetime(2018, 11, 23)
    df1 = features.main_(list_of_companies, NEWSS_DIR, STOCKS_DIR) #Данные, которым нужно расставить метки
    a = predictor.prediction(PICKLE_PATH, df1)
    c = list_of_companies.Company.values
    print('\n')
    for i in range(0, len(a)):
        print(c[i] + (lambda x : ' - вырастет' if x == 1 else ' - упадёт')(a[i]))
    print('\n')

   
if __name__ == '__main__':
     main()
