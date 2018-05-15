import difflib
from flask import json
from cutword import cutw

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
        if t!=[]:
            return t[0].lower()
        elif y!=[]:
            return y[0].lower()
        elif e==[] and y==[]:
            return ''
        else:
            return e[0].lower()
print(checDic('สวัสดี'))