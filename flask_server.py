from flask import Flask, render_template, json
import Main
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

app = Flask(__name__)

MAIN_FILE = 'company.csv'
STOCKS_DIR = getcwd()
NEWS_DIR = getcwd()
NEWSS_DIR = getcwd()
TRAIN_PATH = getcwd()
PICKLE_PATH = getcwd()
DATE_START = 0
DATE_CLOSE = 0

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

@app.route("/")
def hello():
    return render_template('instruction.html')

@app.route("/update/<number>")
def update_data(number):
    Main.update(number)
    return '<HTML><BODY>Updated</BODY></HTML>'

def isrised(number):
    if (number == 1):
        return ' вырастет'
    else:
        return ' упадет'

@app.route("/run")
def run():
    list_of_companies = pd.read_csv(MAIN_FILE)
    names = list(list_of_companies.Company.values)
    DATE_START = datetime.datetime.today() - datetime.timedelta(days = 1)
    DATE_CLOSE = datetime.datetime(2018, 11, 23)
    df1 = features.main_(list_of_companies, NEWSS_DIR, STOCKS_DIR) #Данные, которым нужно расставить метки
    a = predictor.prediction(PICKLE_PATH, df1)
    list_ = []
    for index, name in enumerate(names):
        list_.append(name + isrised(a[index]))
    result = '<br><i>Предсказания:</i><br>'
    for item in list_:
        result += '<br>'
        result += item
    result += '<br><br>'
    return json.dumps(result, ensure_ascii = False)

if __name__ == "__main__":
    app.run()
