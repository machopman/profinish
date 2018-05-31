
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

#print(searchMovieNameInDic('ใครเป็นนักแสดงลอสแองเจอลิส'))

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

def searchM(question):
    question = str(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = load(f)
        e = ''
        for key, value in a.items():
                if question in value:
                    w = key.lower()
                    u  =str(w)
                    e = e+u
    if e !='':
        return e
    elif e =='':
        return question
print(searchM('wonderwoman'))