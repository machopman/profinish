



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
    q = readFile()
    if question in q:
        return 'find'
    else:
        return 'not'

#print(cheEng('piano'))