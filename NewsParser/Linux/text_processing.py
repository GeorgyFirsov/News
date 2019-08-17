from datetime import datetime, timedelta

from string import punctuation
from pymorphy2 import MorphAnalyzer


def lemmatizator(text):
    """This function uses pymorphy2 library to convert
    all words in input text ot normal form for
    further vectorization. All punctuation marks
    are ignored and removed form resulting text

    :param text: plain text to lemmatize
    :return: text after lemmatization: all words were
             converted to their normal form
    """

    exclude = set(punctuation)
    analyzer = MorphAnalyzer()

    text = ''.join(i for i in text if i not in exclude)
    words = text.split()

    converted_text = str()
    for word in words:
        normalized_word = analyzer.parse(word)[0].normal_form
        converted_text += normalized_word + ' '

    return converted_text


def change_date(date):
    """Makes date to be matched the format dd.mm.yyy
    If format already satisfied does nothing
    Otherwise converts date to correct format

    :param date: string with date
    :return: correct date
    """

    if 'назад' not in date:
        return date
    else:
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        day, month, year = today.day, today.month, today.year

        date_digits = [int(s) for s in date.split() if s.isdigit()]

        # Necessary to detect yesterday's news
        # e.g. news was published 15 minutes ago, but now is 00:10 am
        if 'минута' in lemmatizator(date):
            if date_digits[0] > today.minute and today.hour == 0:
                # Yesterday's news
                day, month, year = yesterday.day, yesterday.month, yesterday.year
        else:
            if date_digits[0] > today.hour:
                # Yesterday's news
                day, month, year = yesterday.day, yesterday.month, yesterday.year

        return str(day) + '.' + str(month) + '.' + str(year)
