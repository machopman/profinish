
from googletrans import Translator
import  requests
from cutword import cutw
from json import load
from normalname import checDic
from searchMovieNameInDic import searchMovieNameInDic

def movie_detail(event,findm,question,):
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
                Movie_URL = 'http://mandm.plearnjai.com/API/detailMovie.php?idmovie=' + movie['idIMDb']
                r = requests.get(url=Movie_URL)
                movie_detail = r.json()
                detail = movie_detail['response'][0]['detailMovie'][0]['Synopsis']
                denew  = detail.replace('&nbsp;','')
                denew= denew.replace('\n','')

                if detail != '':
                    for i in range(0, len(denew)):
                        conv = ord(denew[i])
                        if 161 <= conv <= 251:
                            return denew
                        else:
                            translator = Translator()
                            translations = translator.translate(denew, dest='th')
                            return translations.text
                else:
                    return 'ยังไม่ทราบเนื้อเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่ทราบเนื้อเรื่องนี้เลยครับ'
    elif (movie_name == '') and (searchMovieNameInDic(question) == ''):
        mov = findm
        movie_name = mov.lower().replace(' ','')
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
                detail = movie_detail['response'][0]['detailMovie'][0]['Synopsis']
                denew = detail.replace('&nbsp;', '')
                denew = denew.replace('\n', '')

                if detail != '':
                    for i in range(0, len(denew)):
                        conv = ord(denew[i])
                        if 161 <= conv <= 251:
                            return denew
                        else:
                            translator = Translator()
                            translations = translator.translate(denew, dest='th')
                            return translations.text
                else:
                    return 'ยังไม่ทราบเนื้อเรื่องนี้เลยครับ'
        if found == False:
            return 'ยังไม่ทราบเนื้อเรื่องนี้เลยครับ'
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
                                    detail = movie_detail['response'][0]['detailMovie'][0]['Synopsis']
                                    denew = detail.replace('&nbsp;', '')
                                    denew = denew.replace('\n', '')

                                    if detail != '':
                                        for i in range(0, len(denew)):
                                            conv = ord(denew[i])
                                            if 161 <= conv <= 251:
                                                return denew
                                            else:
                                                translator = Translator()
                                                translations = translator.translate(denew, dest='th')
                                                return translations.text
                                    else:
                                        return 'ยังไม่ทราบเนื้อเรื่องนี้เลย'
                            if found == False:
                                    return 'ยังไม่ทราบเนื้อเรื่องนี้เลย'
                    except :
                        return 'ยังไม่ทราบลยครับ'
#print(movie_detail('ขอเรื่องย่อวันเดอ'))