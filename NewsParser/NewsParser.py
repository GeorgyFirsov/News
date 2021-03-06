﻿# This module parses news from web
from threading import Thread, Semaphore
from time import sleep

import unicodecsv as csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

from TextProcessing.TextProcessor import lemmatize, change_date


class NewsParser:
    """This class provides news parsing from site

    Fields:
        __url: url to site with news
        __companies_list_file: file with list of companies
        __store_path: path to directory where news will be saved
        __driver_path: path to Chrome driver
        __semaphore: semaphore, that bounds an amount of simultaneously working threads
    """

    def __init__(self, url: str, companies_list_file: str
                 , store_path: str, driver_path: str
                 , delay: float = 0.25):
        """Constructs parser object.
        It checks if all field are not empty
        and if not, throws an exception.
        """

        if companies_list_file is None \
                or store_path is None \
                or driver_path is None:
            raise Exception("All paths must be specified")

        self.__url = url
        self.__companies_list_file = companies_list_file
        self.__store_path = store_path
        self.__driver_path = driver_path
        self.__delay = delay

        # Semaphore gives us guarantee, that at most
        # 4 threads will run run at the same time
        self.__semaphore = Semaphore(4)

        # will be filled in future
        self.__names = None

    def parse_news(self):
        """Makes main work of this class
        Firstly reads companies from file and than
        parses news for each of them
        """

        self.__get_companies()
        self.__get_news()

    def __process(self, name: str, ticker: str):
        self.__semaphore.acquire()

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        browser = Chrome(executable_path=self.__driver_path, chrome_options=options)
        browser.get(self.__url)

        try:

            search_form = browser.find_element_by_xpath('''/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input''')
            search_form.send_keys(name)
            search_form.send_keys(Keys.ENTER)

            browser.find_element_by_xpath('''/html/body/div[5]/section/div/div[1]/ul/li[3]/a''').click()

            news  = list()
            dates = list()

            # Waiting is necessary, because updated site
            # marks page as loaded before news table is
            # ready. So we need to wait until it loads.
            sleep(self.__delay)

            table = browser.find_element_by_xpath('''/html/body/div[5]/section/div/div[4]/div[3]/div''')
            articles = table.find_elements_by_class_name('articleItem')

            for article in articles:
                text_div = article.find_element_by_class_name('textDiv')
                text = text_div.find_element_by_class_name('title').text
                date = text_div.find_element_by_class_name('articleDetails').find_element_by_class_name('date').text

                news.append(text)
                dates.append(date)

            data = [(replace_dash(change_date(date)), lemmatize(event)) for date, event in zip(dates, news)]

            with open(self.__store_path + 'News' + ticker + '.csv', 'wb') as file:
                writer = csv.writer(file, encoding='utf-8')
                writer.writerow(('Date', 'New'))
                for row in data:
                    writer.writerow(row)

            print('Готово: {}'.format(name))

        finally:
            browser.close()
            self.__semaphore.release()

    def __get_companies(self):
        self.__names = pd.read_csv(self.__companies_list_file, encoding='utf-8')
        if self.__names is None:
            raise Exception("Error reading data frame")

    def __get_news(self):
        names   = self.__names.Company.values
        tickers = self.__names.Ticker.values

        threads = [Thread(target=self.__process, args=(name, ticker,)) for ticker, name in zip(tickers, names)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


# End of NewsParser class --------------------------------------------------


def replace_dash(string: str) -> str:
    return string.replace(' - ', '')


def parse(driver_path: str, file_name: str = None, path: str = None):
    """Main entry point of module. Called from Main.py.

    :param driver_path: path to Chrome driver
    :param file_name: file with list of companies
    :param path: path to directory where news will be saved
    """

    url = 'https://ru.investing.com/'
    parser = NewsParser(url, file_name, path, driver_path)
    parser.parse_news()
