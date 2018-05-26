import difflib

from json import load


import re

from restplus import mmcut
from searchMovieNameInDic import searchMovieNameInDic


def searchMovieName(question):
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', str(question)).replace(' ', '')
    name =  searchMovieNameInDic(question)
    if sentence !='' and name !='':
        cut = mmcut(question)
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
            #print(t[0])
            return t[0]
    else:
        return ''

#searchMovieName("ใครเป็นผู้กำกับวัน")


def checkd(question):
    name = searchMovieName(question)
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', str(question)).replace(' ', '')
    if name !='':
        return name
    elif sentence !='':
        return sentence
    elif sentence =='' and name =='':
        return question
#print(checkd('ใครเป็นนักแสดงวันเดอวูแม'))
#print((checkd('สปอย')))
