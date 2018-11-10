from multiprocessing import Pool
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from time import sleep
 
def get_news(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    dives = soup.find('table', class_='news-list').find_all('div', class_='date')
    dates=[]
    for dive in dives:
        date=dive.text
        dates.append(date)
    dives = soup.find('table', class_='news-list').find_all('div', class_='subject')
    news=[]
    for dive in dives:
        new=dive.text
        news.append(new)
    data=[]
    for i in range(len(news)):
        data.append((dates[i],news[i]))
    print(data)
    return data

def write_csv(data, name):
    with open('News' + name + '.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def write_file(url, name):
    data = get_news(url)
    for i in data:
        write_csv(i,name)

def main():

    #urls=['https://www.finam.ru/profile/moex-akcii/mosenrg/news/#', 'https://www.finam.ru/profile/moex-akcii/gdr-ros-agro-plc-ord-shs/news/?market=1', 'https://www.finam.ru/profile/moex-akcii/pllc-yandex-n-v/news/?market=1', 'https://www.finam.ru/profile/moex-akcii/nornickel-gmk/news/?market=1', 'https://www.finam.ru/profile/moex-akcii/lukoil/news/?market=1']
    url = 'https://www.finam.ru/profile/moex-akcii/megafon-ao/news/'
    name = 'Megafon'
    write_file(url, name)

if __name__ == '__main__':
     main()