import requests
import random

from googletrans import Translator


def searchpic():
    URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
    r = requests.get(url=URL)
    data = r.json()
    q = []
    for movie in data:
        if movie['idIMDb'] !='tt':
           e=movie['idIMDb']
           q.append(e)
    e = random.choice(q)


    Movie_URL = 'http://mandm.plearnjai.com/API/detailMovie.php?idmovie=' +e
    r = requests.get(url=Movie_URL)
    movie_detail = r.json()
    detail1 = movie_detail['response'][0]['detailMovie'][0]['nameEN']
    detail2 = movie_detail['response'][0]['detailMovie'][0]['nameTH']
    detail3 = movie_detail['response'][0]['detailMovie'][0]['Synopsis']

    y = ("https://imagemovie.herokuapp.com/" + e + '.jpg')
    c = "http://www.mandm.plearnjai.com/web/detailMovie.php?nameEN=" + detail1 + "&nameTH=" + detail2

    url = 'http://movieapi.plearnjai.com/DEV/API/Summarization.php?idmovie='+e
    u = requests.get(url=url)
    story = u.json()
    detail4 = story['response']['Review_mandm']
    e =''
    if detail4 != None:
        translator = Translator()
        translations = translator.translate(detail4, dest='th')
        e=e+translations.text
    elif detail4=='':
        t = 'ไม่มีบทวิจารณ์หนังเรื่องนี้นะ'
        e=e+t


    return y ,detail1, detail2,c,detail3 ,e



def send():
    t = []
    url = []
    det = []
    for j in range(6):
        a = searchpic()
        b = a[0]
        t.append(b)
        c = a[1]
        t.append(c)
        d = a[2]
        t.append(d)
        e = a[3]
        url.append(e)
        d = a[4]
        det.append(d)
        f = a[5]
        det.append(f)
    return t ,url , det

#print(searchpic())
#print(send()[0][0])





