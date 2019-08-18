# This file contains creator of directories

from os import system, path

from .Paths import stocks_directory, news_directory, prnews_directory


def make_directories():
    """This function creates directories for parsed stocks,
    parsed news and processed (classified) news.
    Before it function checks if directories exist and doesn't
    perform creation, if they do.
    """

    if not path.exists(stocks_directory):
        system('mkdir ' + stocks_directory)
    if not path.exists(news_directory):
        system('mkdir ' + news_directory)
    if not path.exists(prnews_directory):
        system('mkdir ' + prnews_directory)
