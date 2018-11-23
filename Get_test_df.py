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


#Вот это нужно заменить на импорт этой самой функции
def lemmatizator(text):
    exclude = set(string.punctuation)
    morphy = pymorphy2.MorphAnalyzer()
    text = ''.join(i for i in text if i not in exclude)
    words = text.split()
    new_words = []
    for word in words:
        new_words.append(morphy.parse(word)[0].normal_form)
    new_text = ''
    for word in new_words:
        new_text += word
        new_text +=' '
    return new_text

def main():
    dataframe = pd.read_csv('NewsMagn.csv', sep =',', encoding='utf-8')
    print(text_predict(dataframe).head())

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

#Сюда будем подавать датафрейм из csv файла. Вернется датафрейм, который нужно записать в соответствующий csv файл.
#Желательно в другой, а не News<Company>.csv
def text_predict(dataframe):
    list_ = get_objs()
    clf = list_[0]
    vectorizer = list_[1]
    print('6 done')
    dataframe['label'] = dataframe.New.apply(lambda x: clf.predict(vectorizer.transform([lemmatizator(x)]))[0])
    return dataframe


def get_objs():
    df = pd.read_csv('train\train.csv', sep =';', encoding='utf-8')
    df.New = df.New.apply(lemmatizator)
    print('1 done')
    df.New = df.New.apply(replace_name)
    print('2 done')
    vectorizer = CountVectorizer().fit(df['New'])
    features = vectorizer.transform(df['New'])
    print('3 done')
    clf = LogisticRegression()
    print('4 done')
    clf.fit(features, df.label)
    print('5 done')
    return [clf,vectorizer]


#Функция очень долго работает. Думаю, лучше будет просто один раз убрать все имена компаний и сохранить
def replace_name(string_):
    names = ['Ростелеком', 'Сургутнефтегаз','Мегафон', 'М.Видео', 'ФосАгро', 'Уралкалий', 'СОЛЛЕРС', 'Камаз', 'Энел', 'X5 Retail Group', 'Интер', 'МТС', 'ОАК','Сбербанк', 'Газпром', 'Яндекс']
    new_string = string_
    for name in names:
        new_string = new_string.replace(lemmatizator(name),'')
        print(name + ' was replaced')
    return new_string

if __name__ == '__main__':
    main()


