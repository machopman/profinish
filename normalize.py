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
    if "นนัก" not in word:
        question = re.sub(r'(\w)\1+', r'\1', word)
        s = cutw(question)
        e= GetListWithoutRepetitions(s)
        f = ''
        for i in e:
            f=f+i
        return f
    else:
        s = cutw(word)
        p = []
        for i in s:
            if len(i) > 2:
                p.append(i)
        e = GetListWithoutRepetitions(p)
        k =''
        for i in e:
            k = k +i
        return k




#print(normalword('ใครเป็นนักแสดงงงงงงงงงงวันเดอวูแมนนนนนน'))

#print(normalword('ใครเป็นผู้กำกับบบบบบบวันเดอวูแมนนนนน'))
