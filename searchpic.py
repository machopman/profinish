import requests
import random
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
    y = ("https://imagemovie.herokuapp.com/" + e + '.jpg')
    c = "http://www.mandm.plearnjai.com/web/detailMovie.php?nameEN=" + detail1 + "&nameTH=" + detail2
    return y ,detail1, detail2,c








