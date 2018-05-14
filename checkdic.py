from json import load

from flask import json

from cutword import cutw
import re
def searchMovieNameInDic(question):
    cut = cutw(question)
    ans =''
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = load(f)
        for key, value in a.items():
            for i in cut:
                if i  in value:
                     for i in value:
                         if i in question:
                             ans = ans+question.replace(i,'')
    return ans


def checkd(question):
    name = searchMovieNameInDic(question)
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', question).replace(' ', '')
    if name !='':
        return name
    elif sentence !='':
        return sentence
    elif sentence =='' and name =='':
        return question
#print(checkd('ใครเป็นผู้กำกับวันเดอวูแมน'))

def checDic(question):
    cut = cutw(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = json.load(f)
        e = ''
        for key, value in a.items():
            for i in cut:
                if i in value:
                    w = i
                    u  =str(w)
                    e = e+u
        return e
