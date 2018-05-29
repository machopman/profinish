import re
import requests
def checkname(event):
    movie_name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]','', event).replace(' ', '')
    movie_name = movie_name.lower()
    URL = "http://mandm.plearnjai.com/API/id_nameMovie.php?key=mandm"
    r = requests.get(url=URL)
    data = r.json()
    found = False
    for movie in data:

        nameEN= movie['nameEN'].lower().replace(' ', '')
        if movie_name == nameEN:
            found = True

    return found


#print(checkname('wonderwoman'))