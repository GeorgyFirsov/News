import pymorphy2
import string
from datetime import datetime
from Lemmatizator.Lemmatizator import lemmatizator
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