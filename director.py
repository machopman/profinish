import re

import  requests

from checkName import checksentence
from cutnameword import CutName
from cutword import cutw
from json import load

from classifyname import checDic
from searchMovieNameInDic import searchMovieNameInDic, searchMovie


def movie_director(event,findm,question):
    dd= checDic(event.message.text)
    movie_name = searchMovie(dd)
    e =CutName(question)
    le = len(checksentence(question))
    name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]', '',
                  movie_name).replace(' ', '')
    if e!='' and movie_name !='' and name !='':  #คำถาม+ชื่อภาอังกฤษ
        movie_name = movie_name.lower()
        URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
        r = requests.get(url=URL)
        data = r.json()
        found = False
        for movie in data:
            if movie_name == movie['nameEN'].lower().replace(' ', ''):
                found = True
                Movie_URL = 'http://mandm.plearnjai.com/API/detailMovie.php?idmovie=' + movie['idIMDb']
                r = requests.get(url=Movie_URL)
                movie_detail = r.json()
                detail = movie_detail['response'][0]['detailMovie'][0]['Direct']
                detail = detail.replace('\n', '')
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลยครับ'

    elif (movie_name=='' and le==1 and name ==''):  #คำถามธรรมดา
        print('เข้า2')
        mov = findm
        movie_name = mov.lower().replace(' ','')
        URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
        r = requests.get(url=URL)
        data = r.json()
        found = False
        for movie in data:
            if movie_name == movie['nameEN'].lower().replace(' ', ''):
                print(movie_name)
                found = True
                Movie_URL = 'http://mandm.plearnjai.com/API/detailMovie.php?idmovie=' + movie['idIMDb']
                r = requests.get(url=Movie_URL)
                movie_detail = r.json()
                detail = movie_detail['response'][0]['detailMovie'][0]['Direct']
                detail = detail.replace('\n', '')
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลยครับ'

    elif movie_name !='' and searchMovieNameInDic(movie_name)!='' :
        print('เข้า3')
        with open('new.txt', mode='r', encoding='utf-8-sig') as f:
            a = load(f)
            for key, value in a.items():
                    try:
                        if dd in value:
                            w = key.lower()
                            movie_name = w.lower()
                            URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
                            r = requests.get(url=URL)
                            data = r.json()
                            found = False
                            for movie in data:
                                if movie_name == movie['nameEN'].lower().replace(' ', ''):
                                    found = True
                                    Movie_URL = 'http://mandm.plearnjai.com/API/detailMovie.php?idmovie=' + movie['idIMDb']
                                    r = requests.get(url=Movie_URL)
                                    movie_detail = r.json()
                                    detail = movie_detail['response'][0]['detailMovie'][0]['Direct']
                                    detail = detail.replace('\n', '')
                                    if detail != '':
                                        return detail
                                    else:
                                        return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลย'
                            if found == False:
                                    return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลย'
                    except:
                        return 'ยังไม่รู้ใครเป็นผู้กำกับเลย'
    elif movie_name !='':
        print('เข้า4')
        movie_name = movie_name.lower()
        URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
        r = requests.get(url=URL)
        data = r.json()
        found = False
        for movie in data:
            if movie_name == movie['nameEN'].lower().replace(' ', ''):
                found = True
                Movie_URL = 'http://mandm.plearnjai.com/API/detailMovie.php?idmovie=' + movie['idIMDb']
                r = requests.get(url=Movie_URL)
                movie_detail = r.json()
                detail = movie_detail['response'][0]['detailMovie'][0]['Direct']
                detail = detail.replace('\n', '')
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่มีข้อมูลผู้กำกับหนังเรื่องนี้เลยครับ'
    elif e !='' and dd =='':
        print('เข้า5')
        return 'ยังไม่มีข้อมูลนะครับ'
    else:
        print('เข้า6')
        return 'ยังไม่มีข้อมูลเลยจร้า'






'''
event = 'วันเดอ'
r =checDic(event)  #ใครเป็นผู้กำกับ=''   #  #'ใครเป็นผู้กำกับwonderwoman'=wonderwoman
                    #'ใครเป็นผู้กำกับwonderwom'=wonderwoman #'ใครเป็นผู้กำกับวันเดอ'=วันเดอ
                    #'ใครเป็นผู้กำกับดราก้อนบอล'=''
print(r)
'''
'''
movie_name ='วันเดอ'
movie_name = searchMovie(movie_name) #ใช้เฉพาะมีชื่ออย่างเดียว
print(movie_name)

'''
'''
question ='ใครเป็นผู้กำกับดราก้อนบอล'   #'ใครเป็นผู้กำกับwonderwoman' =wonderwoman  #ชื่อ+คำถามเท่านั้น
e =CutName(question)
print(e)

'''