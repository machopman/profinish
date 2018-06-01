import re
import  requests
from json import load

from checkName import checksentence
from classifyname import checDic
from cutnameword import CutName
from cutword import cutw
from searchMovieNameInDic import searchMovieNameInDic, searchMovie


def movie_actor(event,findm,question):
    dd = checDic(event.message.text)
    movie_name = searchMovie(dd)
    e = CutName(question)
    le = len(checksentence(question))
    name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]', '',
                  movie_name).replace(' ', '')
    if e != '' and movie_name != '' and name != '':  # คำถาม+ชื่อภาอังกฤษ
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
    elif (movie_name == '' and le == 1 and name == ''):  # คำถามธรรมดา
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

    elif movie_name != '' and searchMovieNameInDic(movie_name) != '':
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
    elif movie_name != '':
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
    elif e != '' and dd == '':
        print('เข้า5')
        return 'ยังไม่มีข้อมูลนะครับ'
    else:
        print('เข้า6')
        return 'ยังไม่มีข้อมูลเลยจร้า'






#print(movie_actor('ใครเป็นนักแสดงวันเดอวูแมน,'''))
#print(movie_actor('ใครเป็นนักแสดงwonderwoman'))
















