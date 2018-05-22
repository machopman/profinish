
import  re
import  requests
from cutword import cutw
from json import load
from main import checDic
from searchMovieNameInDic import searchMovieNameInDic
def movie_image(event,findm,question):
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
                return  "https://imagemovie.herokuapp.com/"+movie['idIMDb']+'.jpg'

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
                return "https://imagemovie.herokuapp.com/" + movie['idIMDb'] + '.jpg'
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
                                    return "https://imagemovie.herokuapp.com/" + movie['idIMDb'] + '.jpg'
                    except :
                        return 'ไม่มีรูปเรื่องนี้นะ'
#print(movie_image('ขอรูปหนังwonderwoman'))
