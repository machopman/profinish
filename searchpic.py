import requests
import random
def searchpic():
    URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
    r = requests.get(url=URL)
    data = r.json()
    q = []
    for movie in data:
        if movie['idIMDb'] !='tt':
           y = ("https://imagemovie.herokuapp.com/" + movie['idIMDb'] + '.jpg')
           q.append(y)
    t = random.choice(q)
    return t