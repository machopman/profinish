import difflib
def readFile1(name):
    a=[]
    with open(name, mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line.replace(' ','').replace('\n','')
            a.append(movie_name)
    return a





def diffli(question):
    r = readFile1('ques.txt')
    z = difflib.get_close_matches(question, r)
    if z!=[]:
        return z[0]
    elif z==[]:
        return question
#print(diffli('ใครเป็นผู้กำกับ'))