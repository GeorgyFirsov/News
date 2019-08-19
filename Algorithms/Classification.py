# This file contains news classifier implementation
from threading import Thread

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from TextProcessing.TextProcessor import lemmatize


class Predictor:
    """Class that incapsulates prediction call.

    Fields:
        __vectorizer: vectorizer
        __predictor: predictor (e.g. classifier)
    """

    def __init__(self, predictor, vectorizer):
        self.__predictor = predictor
        self.__vectorizer = vectorizer

    def predict(self, target):
        """Calls prediction function
        on target object.

        :param target: target for prediction

        :return: prediction (e.g. number for classification)
        """

        return self.__predictor.predict(self.__transform(target))[0]

    def __transform(self, target):
        return self.__vectorizer.transform([lemmatize(target)])

# End of Predictor class ---------------------------------------------------


class Classifier:
    """Class that performs main function of this module
    It classifies news into two classes: bad and good

    Fields:
        __list_of_companies: list with names of companies
        __news_path: directory with news
        __prnews_path: directory to store classified news
        __train_path: full path to training dataset
    """

    def __init__(self, companies_list_file, news_path, prnews_path, train_path):
        """Constructs classifier object.
        It checks if all field are not empty
        and if not, throws an exception.
        """

        if companies_list_file is None \
                or news_path is None \
                or prnews_path is None \
                or train_path is None:
            raise Exception("All paths must be specified")

        self.__list_of_companies = pd.read_csv(companies_list_file, encoding='utf-8')
        self.__news_path = news_path
        self.__prnews_path = prnews_path
        self.__train_path = train_path

    def classify(self):
        """Performs main action of this class
        Predictions will be stored in files
        in __prnews_path directory.
        """

        self.__write_predictions()

    def __write_predictions(self):
        tickers = self.__list_of_companies.Ticker.values

        threads = []
        for ticker in tickers:
            threads.append(Thread(target=self.__process, args=(ticker,)))

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

    def __process(self, ticker):
        df = pd.read_csv(self.__news_path + 'News' + ticker + '.csv', encoding='utf-8')
        df = self.__make_predictions(df)

        df.to_csv(self.__prnews_path + 'Newss' + ticker + '.csv', encoding='utf-8', sep=',', index=False)

    def __make_predictions(self, data_frame):
        classifier, vectorizer = make_workers(self.__train_path)

        predictor = Predictor(classifier, vectorizer)
        data_frame['label'] = data_frame.New.apply(predictor.predict)

        return data_frame

# End of Classifier class --------------------------------------------------


def make_workers(train_path):
    """Constructs vectorizer and logistic
    regression model.
    They are ready to use.
    """

    data_frame = pd.read_csv(train_path, sep=';', encoding='utf-8')

    vectorizer = CountVectorizer().fit(data_frame['New'])
    features = vectorizer.transform(data_frame['New'])

    classifier = LogisticRegression()
    classifier.fit(features, data_frame.label)

    return classifier, vectorizer


def classify(main_file_path, news_path, newss_path, train_path):
    """Main entry point of module. Called from Main.py.

    :param main_file_path: file with list of companies
    :param news_path: path to directory with news
    :param newss_path: path to directory where classified news will be saved
    :param train_path: path to training dataset
    """

    classifier = Classifier(main_file_path, news_path, newss_path, train_path)
    classifier.classify()
