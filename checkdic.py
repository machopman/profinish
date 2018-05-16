import difflib
from json import load

from flask import json

from cutword import cutw
import re
def searchMovieNameInDic(question):
    cut = cutw(question)
    ques =question
    t = []
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = load(f)

        for key, value in a.items():

            for i in cut:
                if i in value:
                    w = ques.replace(i,'')
                    t.append(w)
                else:
                    z = difflib.get_close_matches(i, value)
                    if z != []:
                        u = ques.replace(i, '')
                        t.append(u)
    if t ==[]:
        return ''
    else:
        return t[0]




def checkd(question):
    name = searchMovieNameInDic(question)
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', question).replace(' ', '')
    if name !='':
        return name
    elif sentence !='':
        return sentence
    elif sentence =='' and name =='':
        return question
#print(checkd('ขอรีวิวwonderwoman'))

