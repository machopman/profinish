import re

import  requests
from cutword import cutw
from json import load
from classifyname import checDic
from searchMovieNameInDic import searchMovieNameInDic, searchMovie


def movie_enjoy(event,findm,question):
    movie_name = checDic(event.message.text)
    movie_name = searchMovie(movie_name)
    name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]', '',
                  movie_name).replace(' ', '')

    if movie_name != '' and name != '':
        movie_name = movie_name.lower()

        URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
        r = requests.get(url=URL)
        data = r.json()
        found = False
        for movie in data:
            if movie_name == movie['nameEN'].lower().replace(' ', ''):
                found = True
                Movie_URL = 'http://movieapi.plearnjai.com/DEV/API/SentimentScore.php?idmovie=' + movie['idIMDb']
                r = requests.get(url=Movie_URL)
                response = r.json()
                detail = response['response'][0]['storyComment'][0]['positiveCount']
                detail2 = response['response'][0]['storyComment'][0]['negativeCount']
                scorepos= int(detail)
                scoreneg= int(detail2)
                pos = ((scorepos / (scorepos + scoreneg)) * 100)
                neg = ((scoreneg / (scoreneg + scorepos)) * 100)

                if pos ==neg:
                    return 'เฉยๆนะ'
                if pos >=50 and  pos <=75:
                    return 'สนุกนะ'
                elif pos >=76 and  pos <=100:
                    return 'สนุกมาก'
                if neg >=50 and  neg <=75:
                    return 'ไม่สนุก'
                elif neg >=76 and  neg <=100:
                    return 'สนุกมาก'



    elif (movie_name=='')and (searchMovieNameInDic(question)==''):
        mov = findm
        movie_name = mov.lower().replace(' ','')
        URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
        r = requests.get(url=URL)
        data = r.json()
        found = False
        for movie in data:
            if movie_name == movie['nameEN'].lower().replace(' ', ''):
                found = True
                Movie_URL = 'http://movieapi.plearnjai.com/DEV/API/SentimentScore.php?idmovie=' + movie['idIMDb']
                r = requests.get(url=Movie_URL)
                response = r.json()
                detail = response['response'][0]['storyComment'][0]['positiveCount']
                detail2 = response['response'][0]['storyComment'][0]['negativeCount']
                scorepos = int(detail)
                scoreneg = int(detail2)
                pos = ((scorepos / (scorepos + scoreneg))*100 )
                neg = ((scoreneg / (scoreneg + scorepos)) * 100)
                if pos ==neg:
                    return 'เฉยๆนะ'
                if pos >=50 and  pos <=75:
                    return 'สนุก'
                elif pos >=76 and  pos <=100:
                    return 'สนุกมาก'
                if neg >=50 and  neg <=75:
                    return 'ไม่สนุกเลย'
                elif neg >=76 and  neg <=100:
                    return 'ไม่สนุกมาก'

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
                                    Movie_URL = 'http://movieapi.plearnjai.com/DEV/API/SentimentScore.php?idmovie=' + movie['idIMDb']
                                    r = requests.get(url=Movie_URL)
                                    response = r.json()
                                    detail = response['response'][0]['storyComment'][0]['positiveCount']
                                    detail2 = response['response'][0]['storyComment'][0]['negativeCount']
                                    scorepos = int(detail)
                                    scoreneg = int(detail2)
                                    pos = ((scorepos / (scorepos + scoreneg)) * 100)
                                    neg = ((scoreneg / (scoreneg + scorepos)) * 100)
                                    if pos == neg:
                                        return 'ไม่ค่อยนะเฉยๆ'
                                    if pos >= 50 and pos <= 75:
                                        return 'สนุกแน่นอน'
                                    elif pos >= 76 and pos <= 100:
                                        return 'สนุกมากๆเลยนะจะบอกให้'
                                    if neg >= 50 and neg <= 75:
                                        return 'ไม่สนุกเลยครับ'
                                    elif neg >= 76 and neg <= 100:
                                        return 'ไม่สนุกมากๆเลย'


                    except:
                        return 'ไม่รู้นะ'

#print(movie_enjoy('วันเดอวูแมนสนุกไหมครับ'))