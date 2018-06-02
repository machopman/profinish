
from cutword import cutw
from keywords import find_keyword



def keyword(word):
    a = cutw(word)
    dd = []
    if len(a) >2:
        p = find_keyword(a, lentext=1)
        for key, value in p.items():
            dd.append(key)

    if dd!=[]:
        return dd
    else:
        return a


print(keyword('ได้'))





