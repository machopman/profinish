import difflib
import random
import re

import requests
from flask import json

from cutsentence import cutsentence
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

#z = difflib.get_close_matches(i, value)
def checDic(question):
    ques = question
    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', ques).replace(' ', '')
    cut = cutsentence(ques)
    #print(cut)
    if sentence !='':
        name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]', '',question).replace(' ', '')
        if name =='':
            with open('new.txt', mode='r', encoding='utf-8-sig') as f:
                a = json.load(f)
                e = []
                q= []
                for key, value in a.items():
                    try:
                        for i in value:
                            for j in cut:
                                if j in i:
                                    e.append(i)
                                elif e==[]:
                                    z = difflib.get_close_matches(j, value)
                                    if z!=[]:
                                        for n in z:
                                            q.append(n)
                    except:
                        e=e.append('')
                        q.append('')
                if e!=[]:
                    k = []
                    for i in cut:
                       for j in e:
                           if i==j:
                               k.append(j)
                               return j
                    if k==[]:
                        return e[0]
                elif e==[] and q !=[]:
                    return q[0]

                elif e==[] and q==[]:
                    return ''

        elif name!='':
            g= []
            y=[]
            name = name.lower()
            with open('new.txt', mode='r', encoding='utf-8-sig') as f:
                a = json.load(f)
                for key, value in a.items():
                    try:
                        z = difflib.get_close_matches(name, value)
                        if z!=[]:
                            for m in z:
                                y.append(m)
                                if name in m:
                                    g.append(m)
                                else:
                                    y.append(m)
                    except:
                        g = g+''
                        y.append('')

            if g!=[]:
                p = []
                for c in cut:
                    if c in g:
                        p.append(c)
                if p!=[]:
                    return p[0]
                else:
                    return g[0]
            elif y!=[]:
                return y[0]
            else:
                return ''

    else:
         return ''



print(checDic("ใครเป็นผู้กำกับ"))



#checDic('ใครเป็นนักแสดงวันเดอวูแ')

#z = difflib.get_close_matches(i, value)
