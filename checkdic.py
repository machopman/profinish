import difflib
from json import load

from flask import json

from cutword import cutw
import re

from searchMovieNameInDic import searchMovieNameInDic


def searchMovieName(question):
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', question).replace(' ', '')
    name =  searchMovieNameInDic(question)
    if sentence !='' and name !='':
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
    else:
        return ''




def checkd(question):
    name = searchMovieName(question)
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', question).replace(' ', '')
    if name !='':
        return name
    elif sentence !='':
        return sentence
    elif sentence =='' and name =='':
        return question
print(checkd('ขอรีวิวwonderwoman'))

