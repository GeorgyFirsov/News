import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import pandas as pd
import pymorphy2
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn import grid_search
import nltk
import sys
sys.path.append('C:\\Users\\gerko\\Documents\\Project\\News')
from NewsParser.Windows.text_processing import lemmatizator

def main():
    get_labels()
def get_labels():
    company_path = 'C:\\Users\\gerko\\Documents\\Project\\News\\company.csv' #Поменяйте это для себя
    list_of_companies = pd.read_csv(company_path)
    tickers = list_of_companies.Ticker.values
    for ticker in tickers:
        df = pd.read_csv('C:\\Users\\gerko\\Documents\\Project\\News\\NewsP\\News' + ticker +'.csv')
        df = text_predict(df)
        df.to_csv('C:\\Users\\gerko\\Documents\\Project\\News\\NewssP\\Newss' + ticker + '.csv', encoding = 'utf-8', sep =',', index = False)

#Сюда будем подавать датафрейм из csv файла. Вернется датафрейм, который нужно записать в соответствующий csv файл.
#Желательно в другой, а не News<Company>.csv
def text_predict(dataframe):
    list_ = get_objs()
    clf = list_[0]
    vectorizer = list_[1]
    dataframe['label'] = dataframe.New.apply(lambda x: clf.predict(vectorizer.transform([lemmatizator(x)]))[0])
    return dataframe


def get_objs():
    df = pd.read_csv('train.csv', sep =';', encoding='utf-8')
    vectorizer = CountVectorizer().fit(df['New'])
    features = vectorizer.transform(df['New'])
    clf = LogisticRegression()
    clf.fit(features, df.label)
    return [clf,vectorizer]


#Функция очень долго работает. Думаю, лучше будет просто один раз убрать все имена компаний и сохранить
def replace_name(string_):
    names = ['Ростелеком', 'Сургутнефтегаз','Мегафон', 'М.Видео', 'ФосАгро', 'Уралкалий', 'СОЛЛЕРС', 'Камаз', 'Энел', 'X5 Retail Group', 'Интер', 'МТС', 'ОАК','Сбербанк', 'Газпром', 'Яндекс']
    new_string = string_
    for name in names:
        new_string = new_string.replace(lemmatizator(name),'')
        print(name + ' was replaced')
    return new_string

#Эта функция уже не понадобится. Но на всякий оставлю
def change_train():
    df = pd.read_csv('train.csv', sep =';', encoding='utf-8')
    print('''I've got a data''')
    df.New = df.New.apply(lemmatizator)
    print('Lemmatization is done')
    df.New = df.New.apply(replace_name)
    df.to_csv('train1.csv', encoding = 'utf-8', sep =';', index = False)

#Эта тоже не понадобится
def get_much_news():
    url = 'https://ru.investing.com/'
    names = ['Ростелеком', 'Сургутнефтегаз','Мегафон', 'М.Видео', 'ФосАгро', 'Уралкалий', 'СОЛЛЕРС', 'KMAZ', 'Энел', 'FIVEDR', 'Интер', 'МТС', 'UNAC']
    browser = Chrome(executable_path = 'chromedriver.exe')
    df1 = pd.DataFrame({'New':[], 'label': []})
    for name in names:
        browser.get(url)
        try:
            search_form = browser.find_element_by_xpath('''/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input''')
            search_form.send_keys(name)
            search_form.send_keys(Keys.ENTER)
            search_form = browser.find_element_by_xpath('''//*[@id="fullColumn"]/div/div[2]/div[2]/div[1]/a[1]''')
            search_form.click()
            search_form = browser.find_element_by_xpath('''//*[@id="pairSublinksLevel1"]/li[3]/a''')
            search_form.click()
            comp_text = []
            for i in range(5):
                browser.find_element_by_xpath('''//*[@id="paginationWrap"]/div[2]/a[''' + str(i+1) + ''']''').click()
                search_form = browser.find_element_by_xpath('''//*[@id="leftColumn"]/div[8]''')
                list_ = search_form.find_elements_by_class_name('articleItem')
                page_text = []
                for element in list_:
                    page_text.append(element.find_element_by_class_name('textDiv').find_element_by_tag_name('a').text)
                comp_text += page_text
            print(name + ''' is parsed''')
            df = pd.DataFrame({'New': comp_text, 'label': [None]*len(comp_text)})
            df1 = pd.concat([df1, df])
            print(len(df1))
        except:
            print(name + ''' isn't parsed''')
    df1.to_csv('data.csv', encoding = 'utf-8', index = False)

if __name__ == '__main__':
    main()


