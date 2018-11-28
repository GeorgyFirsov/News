#
#   Использование:
#
#   main принимает два параметра:
#
#       fname - путь до файла со списком компаний
#
#       path_ - путь сохранения новостей - папка. Оканчивается на \
#
#   Запуск возможен только из Main.py в связи с расположением драйвера:
#
#           ~\Driver\chromedriver_Windows
#

from multiprocessing import Pool
import csv
from datetime import datetime
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from user_agent import generate_user_agent
from time import sleep
from text_processing import change_date
from text_processing import lemmatizator
import numpy as np
from os import getcwd
from threading import Thread

def processing(url, name, ticker, path_):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = Chrome(executable_path = getcwd() + '/Driver/chromedriver_Windows.exe', chrome_options = options)
    browser.get(url)
    search_form = browser.find_element_by_xpath('''/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input''')
    search_form.send_keys(name)
    search_form.send_keys(Keys.ENTER)
    search_form = browser.find_element_by_xpath('''//*[@id="fullColumn"]/div/div[2]/div[2]/div[1]/a[1]''')
    search_form.click()
    search_form = browser.find_element_by_xpath('''//*[@id="pairSublinksLevel1"]/li[3]/a''')
    search_form.click()
    news = []
    dates = []
    pages_table = browser.find_element_by_xpath('''//*[@id="paginationWrap"]/div[2]''')
    for i in range(2):
        pages_table.find_element_by_link_text(str(i+1)).click()
        table = browser.find_element_by_xpath('''//*[@id="leftColumn"]/div[8]''')
        articles = table.find_elements_by_class_name('articleItem')
        for article in articles:
            text = article.find_element_by_class_name('textDiv').find_element_by_tag_name('a').text
            date = article.find_element_by_class_name('articleDetails').find_element_by_class_name('date').text
            news.append(text)
            dates.append(date)
    data = []
    for i in range(len(news)):
        data.append((replace_shit(change_date(dates[i])), lemmatizator(news[i])))
    with open(path_ + 'News' + ticker + '.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(('Date', 'New'))
        for i in data:
            writer.writerow(i)
    browser.close()
    print(name + ' - done')

def write_file(url, fname, path_):
    if path_ == None:
        raise Exception('Empty path')
    names = get_list_of_companies(fname)
    new_get_news(url, names, path_)

def get_proxy():
    proxies_list = [{'http':'http://'+i} for i in ['67.149.217.254:10200',
                '64.20.74.24:45554','62.37.237.101:8080',
                '180.234.206.77:8080',
                '78.11.85.13:8080','109.188.81.101:8080',
                '139.59.17.113:8080','191.179.147.46:11421',
                '111.68.99.42:8080','80.241.219.66:3128',
                '201.20.94.106:8080','216.229.120.173:45554',
                '116.58.247.31:3128','103.9.115.142:3128',
                '82.164.99.193:10200','80.188.79.138:8080',
                '36.75.113.224:8080',
                '1.20.204.163:8080','97.77.49.151:45554',
                '178.54.44.24:8080',
                '65.182.136.153:45554', '111.76.129.223:808',
                 '203.142.81.205'+':'+'8080', 
                '42.202.35.185'+':'+'8118', '189.16.249.114'+':'+'8080',
                '66.162.122.24'+':'+'8080']]
    return proxies_list[np.random.randint(0, len(proxies_list))]

def get_list_of_companies(string_):
    if string_ == None:
        raise Exception('Path can not be NULL')
    df = pd.read_csv(string_)
    return df

def get_tickers(string_):
    if string_ == None:
        raise Exception('Path can not be NULL')
    df = pd.read_csv(string_)
    return df['Ticker'].values

def replace_shit(string_):
    new_string = string_.replace(' - ','')
    return new_string


def new_get_news(url, data_frame, path_):
    threads = []
    names = data_frame.Company.values
    tickers = data_frame.Ticker.values
    for index, name in enumerate(names):
        newThread = Thread(target = processing, args = (url, name, tickers[index], path_, ))
        threads.append(newThread)
    for i in range(0, len(threads), 4):
        if i < len(threads):
            threads[i].start()
        if i+1 < len(threads):
            threads[i+1].start()
        if i+2 < len(threads):
            threads[i+2].start()
        if i+3 < len(threads):
            threads[i+3].start()
        if i < len(threads):
            threads[i].join()
        if i+1 < len(threads):
            threads[i+1].join()
        if i+2 < len(threads):
            threads[i+2].join()
        if i+3 < len(threads):
            threads[i+3].join()

def main_(fname = None, path_ = None):
    print(fname + ' ' + path_)
    url = 'https://ru.investing.com/'
    write_file(url, fname, path_)