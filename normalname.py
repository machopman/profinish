import difflib
import re

import requests
from flask import json
from cutword import cutw
'''
def check(event):

    URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
    r = requests.get(url=URL)
    data = r.json()
    d= []
    for movie in data:
        nameEN= movie['nameEN'].lower().replace(' ', '')
        d.append(nameEN)

    if event in d:
        return event
    else:
        return ''
'''


def checDic(question):
    question =question.replace(' ', '')
    cut = cutw(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = json.load(f)
        e = []
        t=[]
        for key, value in a.items():
            for i in cut:
                if i in value:
                    t.append(key)
                z = difflib.get_close_matches(i, value)
                if z!=[]:
                    e.append(key)
        y=[]
        for j in cut:
            for k in e:
                if j ==k:
                    y.append(k)



        if e==[] and y==[]:
                return ''
        elif e[0] !='Revolt':
            if t!=[]:
                 o = t[0].lower()
                 return o
            elif y!=[]:
                 u =  y[0].lower()
                 return u
            else:
                r = e[0].lower()
                return r


print(checDic('ใครคือผู้กำกับwonderwoman'))


