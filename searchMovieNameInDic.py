
from cutword import cutw
from json import load
def searchMovieNameInDic(question):
    question = str(question)
    cut = cutw(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = load(f)
        e = ''
        for key, value in a.items():
            for i in cut:
                if i in value:
                    w = key.lower()
                    u  =str(w)
                    e = e+u
        return e


def searchMovie(question):
    question = str(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = load(f)
        e = ''
        for key, value in a.items():
                if question in value:
                    w = key.lower()
                    u  =str(w)
                    e = e+u
        return e
print(searchMovie('ใครเป็นผู้กำกับwonderwoman'))