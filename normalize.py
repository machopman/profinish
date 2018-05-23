import re

from cutword import cutw


def GetListWithoutRepetitions(loInput):
    if loInput==[]:
        return []
    loOutput = []
    if loInput[0] is None:
        oGroupElement=1
    else: # loInput[0]<>None
        oGroupElement=None
    for oElement in loInput:
        if oElement != oGroupElement:
            loOutput.append(oElement)
            oGroupElement = oElement
    return loOutput

def  normalword(word):
    question = re.sub(r'(\w)\1+', r'\1', word)
    s = cutw(question)
    e= GetListWithoutRepetitions(s)
    ans =''
    for i in e:
        ans = ans+i
    return  ans

#print(normalword('รีวิว'))