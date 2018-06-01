import re

import requests


def checkmoiveEn():
    URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
    r = requests.get(url=URL)
    data = r.json()
    namemovie=''

    for i,movie in enumerate(data):
        nameEN= movie['nameEN']
        a=(" "+"("+str(i+1)+")"+' '+nameEN)
        namemovie = namemovie+a
    return namemovie

