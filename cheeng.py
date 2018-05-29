



def readFile():
    a=[]
    with open('DictionEng.txt', mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line.replace(' ','').replace('\n','')
            movie_name = movie_name.lower()
            a.append(movie_name)
    return a

def cheEng(question):
    for i in readFile():
        i = i.lower().replace(' ','')
        if question in i :
            return 'find'
        else:
            return 'not'