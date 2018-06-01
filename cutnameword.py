
from restplus import mmcut
def readFile():
    a=[]
    with open("thaiword.txt", mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line
            a.append(movie_name)
    return a


def CutNameMovie(question):
    cut = mmcut(question)
    if len(cut) ==2:
        print('k')
        d= []
        for i in readFile():
            for j in cut:
                if j in i:
                    d.append(j)
        if d!=[]:
            r =question.replace(d[0],'')
            w= question.replace(r,'')
            return w
        else:
            return question
    else:
        return question
#print(CutNameMovie('ใครเป็นผู้กำกับ'))

def CutName(question):
    cut = mmcut(question)
    d= []
    for i in readFile():
        for j in cut:
            if j in i:
                d.append(j)
    if d!=[]:
        r =question.replace(d[0],'')
        return r
    else:
        return ''


#print(CutName('ใครเป็นผู้กำกับ'))