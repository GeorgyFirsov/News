import pandas as pd
from flask import Flask, render_template, json

import StocksParser.StocksParser as StocksParser
import NewsParser.NewsParser as NewsParser
import Algorithms.Classification as Classifier
import Algorithms.CreateFeatures as Features
import Algorithms.Predict as Predictor
from Utilites.MakeDirectories import make_directories
from Utilites.Paths import *


server = Flask(__name__)


@server.route('/run')
def run():
    """Displays result of predictions on website.
    Before this action it calls features creator
    and predictor to analyse parsed data.
    """

    list_of_companies = pd.read_csv(companies_file, encoding='utf-8')
    names = list(list_of_companies.Company.values)

    data_frame = Features.create(list_of_companies, prnews_directory, stocks_directory)
    predictions = Predictor.prediction(binary_path, data_frame)

    predictions_list = list()

    for name, prediction in zip(names, predictions):
        prediction_string = "{} - {}".format(name, prediction_to_string(prediction))
        predictions_list.append(prediction_string)

    page_code = render_result(predictions_list)

    return json.dumps(page_code, encoding='utf-8', ensure_ascii=False)


@server.route('/')
def main_page():
    """Displays main page on website
    """

    return render_template('instruction.html', encoding='utf-8')


@server.route('/update/<parameter>')
def update_server(parameter):
    """This function performs data update.
    If passed '2' it does nothing.
    Otherwise if passed something that differs from 1
    displays an error.
    """

    if parameter == '2':
        return ' '
    if parameter != '1':
        return 'Allowed answers: 1 or 2'

    StocksParser.parse(companies_file, stocks_directory)

    print('\nWaiting for news... It may take a while\n')

    NewsParser.parse(driver_path, companies_file, news_directory)
    Classifier.classify(companies_file, news_directory, prnews_directory, train_set_path)

    return 'Updated'


def render_result(predictions_list):
    """This function reads html code of result page and inserts predictions
    to marked by special comment place.

    :param predictions_list: list of strings with companies and predictions

    :return: html code of page to display
    """

    predictions_string = str()
    for prediction in predictions_list:
        predictions_string += '<br> ' + prediction + '\n'

    with open('./templates/results.html', 'r', encoding='utf-8') as code:
        page_code = code.read()
        page_code = page_code.replace('<!-- insert here-->', predictions_string)
        page_code = page_code.replace('\n', '')

    return page_code


def prediction_to_string(value):
    return 'вырастет' if value else 'упадёт'


if __name__ == "__main__":
    """Main code of this file
    It starts a server
    """

    make_directories()

    server.run()
