from flask import Flask, render_template, json
import Main
import pandas as pd
from os import getcwd
from os import system
from sys import platform
from sys import path
if platform == "linux" or platform == "linux2":
    path.insert(0, getcwd() + '/NewsParser/Linux')
elif platform == "win32":
    path.insert(0, getcwd() + '/NewsParser/Windows')
import Algorithms.CreateFeatures as features
import Algorithms.Predict as predictor

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
    TRAIN_PATH += '/Algorithms/train.csv'
    PICKLE_PATH += '/Algorithms/Predictor.pickle'
elif platform == "win32":
    STOCKS_DIR += '\\StocksP\\'
    NEWS_DIR += '\\NewsP\\'
    NEWSS_DIR += '\\NewssP\\'
    TRAIN_PATH += '\\Algorithms\\train.csv'
    PICKLE_PATH += '\\Algorithms\\Predictor.pickle'

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
    return Main.update(number)

def isrised(number):
    if (number == 1):
        return ' вырастет'
    else:
        return ' упадет'

@app.route("/run")
def run():
    list_of_companies = pd.read_csv(MAIN_FILE)
    names = list(list_of_companies.Company.values)
    df1 = features.create(list_of_companies, NEWSS_DIR, STOCKS_DIR) #Данные, которым нужно расставить метки
    a = predictor.prediction(PICKLE_PATH, df1)
    list_ = []
    for index, name in enumerate(names):
        list_.append(name + isrised(a[index]))
    result = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Предсказания</title><style>body {background: #c7b39b url(https://i.ytimg.com/vi/iYJ2mFlpC20/maxresdefault.jpg); color: #000; height: 500; width: 1000; }</style></head><body><br><b><i>Предсказания:</i></b><br>'''
    for item in list_:
        result += '<br>'
        result += item
    result += '<br><br></body></html>'
    return json.dumps(result, ensure_ascii = False)

if __name__ == "__main__":
    app.run()
