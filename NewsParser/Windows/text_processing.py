import pymorphy2
import string
from datetime import datetime
import pymorphy2
import string

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

def change_date(date):
    if 'назад' in date:
        if 'минута' in lemmatizator(date):
            if [int(s) for s in date.split() if s.isdigit()][0] > datetime.today().minute:
                if datetime.today().hour == 0:
                    result = str(datetime.today().day - 1) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
                else:
                    result = str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
            else:
                result = str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
        else:
            if [int(s) for s in date.split() if s.isdigit()][0] > datetime.today().hour:
                result = str(datetime.today().day - 1) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
            else:
                result = str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
        return result
    else:
        return date