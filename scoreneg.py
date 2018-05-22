
import  re
import  requests
from cutword import cutw
from json import load

from classifyname import checDic
from searchMovieNameInDic import searchMovieNameInDic

def movie_scoreneg(event,findm,question):
    movie_name = checDic(event.message.text)
    if movie_name != '':
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
                #detail = response['response'][0]['allComment'][0]['positiveCount']
                detail2 = response['response'][0]['allComment'][0]['negativeCount']
                detail2 = detail2.replace('\n','')

                if detail2 != '':
                    return detail2
                else:
                    return 'ยังไม่มีคะแนนด้านลบครับ'
        if found == False:
            return 'ยังไม่มีคะแนนด้านลบครับ'
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
                # detail = response['response'][0]['allComment'][0]['positiveCount']
                detail2 = response['response'][0]['allComment'][0]['negativeCount']
                detail2 = detail2.replace('\n', '')

                if detail2 != '':
                    return detail2
                else:
                    return 'ยังไม่มีคะแนนด้านลบครับ'
        if found == False:
            return 'ยังไม่มีคะแนนด้านลบครับ'
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
                                    # detail = response['response'][0]['allComment'][0]['positiveCount']
                                    detail2 = response['response'][0]['allComment'][0]['negativeCount']
                                    detail2 = detail2.replace('\n', '')

                                    if detail2 != '':
                                        return detail2
                                    else:
                                        return 'ยังไม่มีคะแนนด้านลบ'
                            if found == False:
                                 return 'ยังไม่มีคะแนนด้านลบ'
                    except :
                        return 'ยังไม่ทราบคะแนน'
#print(movie_scoreneg('คะแนนลบwonderwoman'))