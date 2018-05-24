import re

from cutword import cutw


def GetListWithoutRepetitions(question):
    if question==[]:
        return []
    Output = []
    if question[0] is None:
        GroupElement=1
    else: # loInput[0]<>None
        GroupElement=None
    for Element in question:
        if Element != GroupElement:
            Output.append(Element)
            GroupElement = Element
    return Output

def  normalword(word):
    question = re.sub(r'(\w)\1+', r'\1', word)
    s = cutw(question)
    e= GetListWithoutRepetitions(s)
    ans =''
    for i in e:
        ans = ans+i
    return  ans

print(normalword('สปอย'))