﻿from os import getcwd
from threading import Thread

import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

from TextProcessing.TextProcessor import lemmatize, change_date


def replace_dash(string):
    return string.replace(' - ', '')


class NewsParser:
    """This class provides news parsing from site

    Fields:
        url: url to site with news
        companies_list_file: file with list of companies
        store_path: path to directory where news will be saved
        driver_path: relative path to Chrome driver
    """

    def __init__(self, url, companies_list_file
                 , store_path, driver_path):
        """Constructs parser object.
        It checks if all field are not empty
        and if not, throws an exception.
        """
        if companies_list_file is None \
                or store_path is None  \
                or driver_path is None:
            raise Exception("All paths must be specified")

        self.url = url
        self.companies_list_file = companies_list_file
        self.store_path = store_path
        self.driver_path = driver_path

        # will be filled in future
        self.names = None

    def parse_news(self):
        """Makes main work of this class
        Firstly reads companies from file and than
        parses news for each of them
        """
        self.__get_companies()
        self.__get_news()

    def __process(self, name, ticker):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        browser = Chrome(executable_path=getcwd() + self.driver_path, chrome_options=options)
        browser.get(self.url)

        search_form = browser.find_element_by_xpath('''/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input''')
        search_form.send_keys(name)
        search_form.send_keys(Keys.ENTER)
        search_form = browser.find_element_by_xpath('''//*[@id="fullColumn"]/div/div[2]/div[2]/div[1]/a[1]''')
        search_form.click()
        search_form = browser.find_element_by_xpath('''//*[@id="pairSublinksLevel1"]/li[3]/a''')
        search_form.click()

        pages_table = browser.find_element_by_xpath('''//*[@id="paginationWrap"]/div[2]''')

        news = []
        dates = []

        # Make 3 attempts to get data
        for i in range(2):
            pages_table.find_element_by_link_text(str(i + 1)).click()
            table = browser.find_element_by_xpath('''//*[@id="leftColumn"]/div[8]''')
            articles = table.find_elements_by_class_name('articleItem')

            for article in articles:
                text = article.find_element_by_class_name('textDiv').find_element_by_tag_name('a').text
                date = article.find_element_by_class_name('articleDetails').find_element_by_class_name('date').text
                news.append(text)
                dates.append(date)

        data = [(replace_dash(change_date(date)), lemmatize(event)) for date, event in zip(dates, news)]

        with open(self.store_path + 'News' + ticker + '.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(('Date', 'New'))
            for row in data:
                writer.writerow(row)

        browser.close()
        print(name + ' - готово')

    def __get_companies(self):
        self.names = pd.read_csv(self.companies_list_file)
        if self.names is None:
            raise Exception("Error reading data frame")

    def __get_news(self):
        names = self.names.Company.values
        tickers = self.names.Ticker.values

        threads = []
        for ticker, name in zip(tickers, names):
            threads.append(Thread(target=self.__process, args=(name, ticker, )))

        for i in range(0, len(threads), 4):
            if i < len(threads):
                threads[i].start()
            if i + 1 < len(threads):
                threads[i + 1].start()
            if i + 2 < len(threads):
                threads[i + 2].start()
            if i + 3 < len(threads):
                threads[i + 3].start()
            if i < len(threads):
                threads[i].join()
            if i + 1 < len(threads):
                threads[i + 1].join()
            if i + 2 < len(threads):
                threads[i + 2].join()
            if i + 3 < len(threads):
                threads[i + 3].join()


def main(driver_path, file_name=None, path=None):
    """Main entry point of file. Called from Main.py

    :param driver_path: relative path to Chrome driver
    :param file_name: file with list of companies
    :param path: path to directory where news will be saved
    """

    url = 'https://ru.investing.com/'
    parser = NewsParser(url, file_name, path, driver_path)
    parser.parse_news()

