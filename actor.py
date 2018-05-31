import re

import  requests
from json import load

from checkName import checksentence
from checkdic import checkd
from classifyname import checDic
from cutword import cutw
from searchMovieNameInDic import searchMovieNameInDic, searchMovie


def movie_actor(event,findm,question):
    movie_name = checDic(event)
    movie_name = searchMovie(movie_name)

    name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]', '',movie_name).replace(' ', '')

    if movie_name != '' and name != '':
        print('เข้า1')
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
                detail = movie_detail['response'][0]['detailMovie'][0]['Actor']
                detail = detail.replace('\n', '')
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลยครับ'
    elif (name == '' and movie_name==''and len(checksentence(question)==1)) :
            print('เข้า2')
            mov = findm
            movie_name = mov.lower().replace(' ', '')
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
                    detail = movie_detail['response'][0]['detailMovie'][0]['Actor']
                    detail = detail.replace('\n', '')
                    print(detail)
                    if detail != '':
                        return detail
                    else:
                        return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลยครับ'
            if found == False:
                return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลยครับ'


    else:
            print('เข้า3')
            cut = cutw(event.message.text)
            with open('new.txt', mode='r', encoding='utf-8-sig') as f:
                a = load(f)
                for key, value in a.items():
                    for i in cut:
                        try:
                            if i in value:
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
                                        detail = movie_detail['response'][0]['detailMovie'][0]['Actor']
                                        detail = detail.replace('\n', '')
                                        print(detail)
                                        if detail != '':
                                            return detail
                                        else:
                                            return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลย'
                                if found == False:
                                    return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลย'
                        except :
                            return 'ยังไม่มีข้อมูลเลย'






#print(movie_actor('ใครเป็นนักแสดงวันเดอวูแมน,'''))
#print(movie_actor('ใครเป็นนักแสดงwonderwoman'))
















