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
    t= ''
    for i in e:
        if len(i)>1:
            t=t+i
    return t

print(normalword('เธอเธอไปไหนไหนมาครับบบบบบบบบบบบบบบบบบบบบ'))