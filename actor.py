
import  re
import  requests
from cutword import cutw
from json import load
from namemoviebefore  import findmovie
from searchMovieNameInDic import searchMovieNameInDic

def movie_actor(event,question,userid):
    movie_name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]','',event.message.text).replace(' ', '')
    if movie_name!='':
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
    elif (movie_name=='')and (searchMovieNameInDic(question)==''):
        mov = findmovie(userid)
        print(mov)
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


    else:
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
                                    if detail != '':
                                        return detail
                                    else:
                                        return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลย'
                            if found == False:
                                return 'ยังไม่มีข้อมูลนักแสดงหนังเรื่องนี้เลย'
                    except :
                        return 'ยังไม่มีข้อมูลเลย'






#print(movie_actor('ใครเป็นนักแสดงวันเดอวูแมน'))
#print(movie_actor('ใครเป็นนักแสดงwonderwoman'))
















