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

