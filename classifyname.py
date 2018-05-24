import difflib
import re
from flask import json
from restplus import mmcut

def checDic(question):
        ques = str(question)
        cut = mmcut(ques)
        k = set(cut)
        f = readFile()
        s = k - f
        cut = list(s)
        if cut!=[]:
            name = re.sub('[ฤกขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]', '',str(ques)).replace(' ', '')
            if name =='':
                with open('new.txt', mode='r', encoding='utf-8-sig') as f:
                    a = json.load(f)
                    e = []
                    q= []
                   # t = []
                    #l=[]
                    for key, value in a.items():
                        try:
                            for i in value:
                                for j in cut:
                                    if j in i:
                                        e.append(i)
                                        #l.append(j)


                                    elif e==[]:

                                        z = difflib.get_close_matches(j, value)
                                        if z!=[]:
                                            for n in z:
                                                #print(j)
                                                #t.append(j)
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
                            z = key.get_close_matches(name, value)
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
                    return ques
        else:
            return ''

def readFile():
    a=[]
    with open('delword.txt', mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line.replace(' ','').replace('\n','')
            a.append(movie_name)

    w = set(a)
    return w
def readFile1():
    a = []
    with open('dictionary.txt', mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line.replace(' ', '').replace('\n', '')
            a.append(movie_name)


    return a
#print(checDic("สปอย"))

'''
for i in readFile1():
    e = checDic(i)
    if e !='':
        print(e)
'''

''''
def write_list():
    with open("sen.txt",mode='w',encoding='utf-8-sig') as f:
        for m in h :
            f.write(m)
'''