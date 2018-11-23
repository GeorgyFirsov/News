﻿from urllib.request import urlopen
from pandas import DataFrame, read_csv
from datetime import datetime
from datetime import timedelta
import pandas as pd
from time import sleep
from os import getcwd
from threading import Thread

DELAY = 8      # диапазон считывания
DELTA_DAYS = 7 # начинаем считывать с DELTA_DAYS дней назад

def make_url(market_, em_, code_, df_, mf_, yf_, from_, dt_, mt_, yt_, to_, f_, p_, e_, cn_, dtf_, tmf_, MSOR_, mstime_, mstimever_):
    url = "http://export.finam.ru/"
    url += f_
    url += ".csv?market="
    url += str(market_)
    url += "?&em="
    url += str(em_)
    url += "&code="
    url += code_
    url += "&apply=0&df="
    url += str(df_)
    url += "&mf="
    url += str(mf_)
    url += "&yf="
    url += str(yf_)
    url += "&from="
    url += from_
    url += "&dt="
    url += str(dt_)
    url += "&mt="
    url += str(mt_)
    url += "&yt="
    url += str(yt_)
    url += "&to="
    url += to_
    url += "&p="
    url += str(p_)
    url += "&f="
    url += f_
    url += "&e=.csv&cn="
    url += code_
    url += "&dtf="
    url += str(dtf_)
    url += "&tmf="
    url += str(tmf_)
    url += "&MSOR="
    url += str(MSOR_)
    url += "&mstime="
    url += mstime_
    url += "&mstimever="
    url += str(mstimever_)
    url += "&sep=1&sep2=1&datf=1&at=1"
    return url

def processing(path_, row, market, df, mf, yf, startDate, dt, mt, yt, endDate):
    fn = row[1] + str(datetime.today().day) + str(datetime.today().month) + str(datetime.today().year) + str(datetime.now().second) + str(datetime.now().minute) + str(datetime.now().hour)
    url = make_url(market, row[2], row[1], df, mf, yf, startDate, dt, mt, yt, endDate, fn, DELAY, '.csv', row[1], 2, 1, 1, 'on', 1)
    sleep(0.8)
    data = read_csv(url)
    cols = data.columns
    data = data.drop(data.columns[[1,3]], axis = 1)
    data.columns = ['' + i for i in ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    toSaveName = path_ + 'Stocks' + row[1] + ".csv"
    data.to_csv(toSaveName)
    print(row[1] + ' - done')

def get_dataFrame(fname, path_):
    if fname == None:
        raise Exception('Path can not be NULL')
    if path_ == None:
        raise Exception('Empty path')
    tdt = datetime.today()
    sdt = tdt - timedelta(days = DELTA_DAYS)
    del tdt
    sdt = sdt.date()
    startDate = str(sdt.day) + '.' + str(sdt.month) + '.' + str(sdt.year)
    endDate = str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)

    df = sdt.day
    mf = sdt.month - 1
    yf = sdt.year
    dt = datetime.today().day
    mt = datetime.today().month - 1
    yt = datetime.today().year
    market = 1

    Data = pd.read_csv(fname)
    Data = Data.drop('Company', axis = 1)

    threads = []

    for row in Data.itertuples():
        nt = Thread(target = processing, args = (path_, row, market, df, mf, yf, startDate, dt, mt, yt, endDate, ))
        threads.append(nt)
    
    count = len(threads)

    for i in range(0, count, 1):
        if i < count:
            threads[i].start()
        if i < count:
            threads[i].join()
        

def main_(fname = None, path_ = None):
    get_dataFrame(fname, path_)
