# This file contains creator of directories

from os import system

from .Paths import stocks_directory, news_directory, prnews_directory


def make_directories():
    """This function creates directories for parsed stocks,
    parsed news and processed (classified) news
    """
    system('mkdir ' + stocks_directory)
    system('mkdir ' + news_directory)
    system('mkdir ' + prnews_directory)
