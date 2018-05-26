import re

import  requests
from json import load



def movie_actor(chec,name,moviename,findm):
    if  name != '' and moviename =='' and chec!='': #มีชื่ออังกฤษด้วย
        movie_name = name.lower()
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
    elif (moviename=='')and (chec=='') and (name==''):
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
                detail = movie_detail['response'][0]['detailMovie'][0]['Actor']
                detail = detail.replace('\n', '')
                print(detail)
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลยครับ'


        elif moviename!='' and name=='' and chec!='' :
            with open('new.txt', mode='r', encoding='utf-8-sig') as f:
                a = load(f)
                for key, value in a.items():
                        try:
                            if moviename in value:
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
















