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
from user_agent import generate_user_agent
from time import sleep
import numpy as np
 
def get_news(url, index):
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
    sleep(np.random.random())
    r = requests.get(url,headers={'User-Agent': generate_user_agent()},
                               proxies=proxies_list[index%len(proxies_list)])
    soup = BeautifulSoup(r.text, "html.parser")
    dives = soup.find('div', class_='js-section-content largeTitle').find_all('div', class_='articleItem')
    dates = []
    for dive in dives:
        date = dive.find('time', class_='date').text
        dates.append(date)
    dives = soup.find('div', class_='js-section-content largeTitle').find_all('div', class_='articleItem')
    news=[]
    for dive in dives:
        new = dive.find('a', class_='title').text
        news.append(new)
    data=[]
    for i in range(len(news)):
        data.append((dates[i],news[i]))
    return data
    

def write_csv(data, name):
    with open('News' + name + '.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def write_file(url, name, index):
    data = get_news(url, index)
    for i in data:
        write_csv(i,name)

def get_links(url, names):
    links = []
    browser = Chrome(executable_path="chromedriver")
    for name in names:
        browser.get(url)
        search_form = browser.find_element_by_xpath('''/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input''')
        search_form.send_keys(name)
        search_form.send_keys(Keys.ENTER)
        sleep(2)
        news_target = browser.find_element_by_xpath('''//*[@id="searchPageResultsTabs"]/li[3]/a''')
        news_target.click()
        link = browser.current_url
        links.append(link)
    return links

def main():
    names = ['Магнит', 'Мегафон', 'Газпром']
    url='https://ru.investing.com/'
    links = get_links(url,names)
    for index, link in enumerate(links):
        write_file(link,names[index], index)
if __name__ == '__main__':
     main()