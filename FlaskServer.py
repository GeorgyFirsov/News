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
    list_of_companies = pd.read_csv(companies_file)
    names = list(list_of_companies.Company.values)

    df1 = Features.create(list_of_companies, prnews_directory, stocks_directory)
    predictions = Predictor.prediction(binary_path, df1)

    predictions_list = list()

    for name, prediction in zip(names, predictions):
        prediction_string = "{} - {}".format(name, prediction_to_string(prediction))
        predictions_list.append(prediction_string)

    page_code = render_result(predictions_list)

    return json.dumps(page_code, ensure_ascii=False)


@server.route('/')
def __main_page():
    return render_template('instruction.html')


@server.route('/update/<parameter>')
def __update_server(parameter):
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

    with open('./templates/results.html', 'r') as code:
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
