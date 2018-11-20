from multiprocessing import Pool
import csv
from datetime import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from user_agent import generate_user_agent
from time import sleep
from text_processing import change_date
from text_processing import lemmatizator
import numpy as np
 
def get_news(url):
    sleep(np.random.random())
    r = requests.get(url,headers={'User-Agent': generate_user_agent()},
                               proxies=get_proxy())
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', class_ = 'js-section-content largeTitle')
    print(div)

def write_file(url, names):
    data_list = new_get_news(url, names)
    for index, data in enumerate(data_list):
        with open('News' + names[index] + '.csv','w') as f:
            writer = csv.writer(f)
            for i in data:
                writer.writerow(i)

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

def new_get_news(url, names):
    browser = Chrome(executable_path="../Linux/chromedriver")
    data_list = []
    for name in names:
        browser.get(url)
        search_form = browser.find_element_by_xpath('''/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input''')
        search_form.send_keys(name)
        search_form.send_keys(Keys.ENTER)
        sleep(1)
        news_target = browser.find_element_by_xpath('''//*[@id="searchPageResultsTabs"]/li[3]/a''')
        news_target.click()
        sleep(1)
        news = []
        for i in range(20):
            new_article = browser.find_element_by_xpath('''//*[@id="fullColumn"]/div/div[4]/div[3]/div/div[''' + str(i+1) + ''']/div/a''')
            new_element = new_article.text
            news.append(new_element)
        dates = []
        for i in range(20):
            new_article = browser.find_element_by_xpath('''//*[@id="fullColumn"]/div/div[4]/div[3]/div/div[''' + str(i+1) + ''']/div/div/time''')
            new_element = new_article.text
            dates.append(new_element)
        data = []
        for i in range(len(news)):
            data.append((change_date(dates[i]), lemmatizator(news[i])))
        data_list.append(data)
    browser.close
    return data_list

def get_list_of_companies(string_):
    data = pd.read_csv(string_)
    data = data.drop('Ticker', axis = 1).drop('Number', axis = 1)
    result = []
    for row in data.itertuples():
        result.append(row[1])
    return result

def main():
    names = get_list_of_companies('../../company.csv')
    url = 'https://ru.investing.com/'
    write_file(url, names)


if __name__ == '__main__':
     main()