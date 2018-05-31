

import requests


def searchstory():
    URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
    r = requests.get(url=URL)
    data = r.json()
    k=[]
    for movie in data:
        if movie['idIMDb'] !='tt':
           e=movie['nameEN']
           k.append(e)
    t = ''
    count = 1
    for i in k:
        t=t+"("+str(count)+")"+" " +i+" "
        count = count + 1
    return t




#print(searchpic())

