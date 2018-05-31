import re

import  requests

from checkName import checksentence
from cutword import cutw
from json import load

from classifyname import checDic
from searchMovieNameInDic import searchMovieNameInDic, searchMovie


def movie_scorepos(event,findm,question):
    movie_name = checDic(event.message.text)
    movie_name = searchMovie(movie_name)
    le = len(checksentence(question))

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
                detail = response['response'][0]['allComment'][0]['positiveCount']
                detail = detail.replace('\n','')

                #detail2 = response['response'][0]['allComment'][0]['negativeCount']
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีคะแนนด้านบวกครับ'
        if found == False:
            return 'ยังไม่มีคะแนนด้านบวกครับ'
    elif (name == '' and movie_name==''and le==1):
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
                detail = response['response'][0]['allComment'][0]['positiveCount']
                detail = detail.replace('\n', '')

                # detail2 = response['response'][0]['allComment'][0]['negativeCount']
                if detail != '':
                    return detail
                else:
                    return 'ยังไม่มีคะแนนด้านบวกครับ'
        if found == False:
            return 'ยังไม่มีคะแนนด้านบวกครับ'
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
                                    detail = response['response'][0]['allComment'][0]['positiveCount']
                                    detail = detail.replace('\n', '')

                                    # detail2 = response['response'][0]['allComment'][0]['negativeCount']
                                    if detail != '':
                                        return detail
                                    else:
                                        return 'ยังไม่มีคะแนนด้านบวก'
                            if found == False:
                                    return 'ยังไม่มีคะแนนด้านบวก'
                    except :
                        return 'ยังไม่รู้คะแนนเลย'
#print(movie_scorepos('อยากได้คะแนนบวกวันเดอวูแมน'))