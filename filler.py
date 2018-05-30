
'''
def readFile1(name):
    a=[]
    with open(name, mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line.replace(' ','').replace('\n','')
            a.append(movie_name)
    return a

xx = readFile1('keyword8.txt')
print(xx)
'''
import difflib

from actor import movie_actor
from date import movie_date
from detail import movie_detail
from director import movie_director
from image import movie_image
from review import movie_review
from spoil import movie_spoil
from type import movie_type

a ={'0':['แสดงนำ', 'ดาราหนัง', 'ตัวประกอบ', 'ตัวละคร', 'แสดงละคร', 'ผู้แสดง', 'แสดง', 'ดารา', 'ดาราภาพยนตร์', 'รับบท', 'การแสดง', 'นักแสดง', 'ภาพยนตร์', 'นักแสดงหลัก'],
    '1':['ผู้ควบคุม', 'คนเขียนบท', 'กำกับ', 'ผู้กำกับภาพยนตร์', 'ผู้กำกับหนัง', 'ผู้กำกับ', 'ผู้เขียนบท', 'ครับ', 'สร้างเรื่อง', 'ผู้เขียนบทภาพยนตร์', 'ผู้เขียนบทหนัง'],
    '2':['รูปงาม', 'รูปภาพ', 'คำถาม', 'ภาพ', 'ภาพถ่าย', 'รูป', 'ได้รูป'],
    '3':['รี', 'วิว', 'review', 'วิจารณ์', 'เล่าเรื่อง', 'แสดงความคิดเห็น', 'ผู้วิจารณ์', 'คิดเห็น', 'ความคิด', 'จาร', 'คำวิจารณ์', 'บทความ', 'นักวิจารณ์', 'บทวิจารณ์', 'วิพากษ์', 'ความคิดเห็น', 'การแสดงความคิดเห็น'],
    '4':['ส่วนสำคัญ', 'จุดสำคัญ', 'เรื่องสำคัญ', 'ประเด็นสำคัญ', 'Spoil', 'spoil', 'พูดถึง', 'สำคัญ'],
    '5':['ลาย', 'เนื้อหนัง', 'เรื่องเล่า', 'เนื้อหา', 'เนื้อความ', 'ย่อ', 'เรื่องราว', 'เล่า', 'เนื้อเรื่อง', 'ย่อความ', 'เรื่องย่อ', 'รายละเอียด', 'เอียด', 'เล่าเรื่อง', 'ละเอียด'],
    '6':['ฉาย', 'ฉายหนัง', 'เมื่อไหร่', 'ขอเวลา', 'วันที่', 'เวลา', 'เมื่อ', 'ออกอากาศ', 'เมื่อไร', 'อากาศ', 'วัน', 'โมง'],
    '7':['ประเภท', 'Type', 'เภท', 'แนว', 'หมวด', 'หมวดหมู่', 'type']}


'''

def filter(cut,clas,event,findm,question):
    t =[]
    for key ,value in a.items():
        for i in cut:
            for  j in value:
               if i in j:
                   t.append(key)

    if t!=[]:
        return t[0]
'''
'''
        if clas == '0':
            if t[0]!='0':
                return clas(t[0],event,findm,question)
            elif  t[0] =='0':
                return ''

        if clas =='1':
            if t[0]!='1':
                return clas(t[0],event,findm,question)
            elif  t[0] =='1':
                return ''


        if clas =='2':
            if t[0] !='2':
                return clas(t[0],event,findm,question)
            elif t[0] == '2':
                return ''

        if clas == '3':
            if t[0] != '3':
                return clas(t[0],event,findm,question)
            elif t[0] == '3':
                return ''

        if clas == '4':
            if t[0] != '4':
                return clas(t[0],event,findm,question)
            elif t[0] == '4':
                return ''

        if clas == '5':
            if t[0] != '5':
                return clas(t[0],event,findm,question)
            elif t[0] == '5':
                return ''

        if clas == '6':
            if t[0] != '6':
                return clas(t[0],event,findm,question)
            elif t[0] == '6':
                return ''

        if clas == '7':
            if t[0] != '7':
                return clas(t[0],event,findm,question)
            elif t[0] == '7':
                return ''

    elif  t==[]:
        return ''
    else:
        return ''
'''

'''

def clss (value,event,findm,question):
    if value =='0':
        return movie_actor(event,findm,question)
    elif value =='1':
        return movie_director(event,findm,question)
    elif value =='2':
        return movie_image(event,findm,question)
    elif value =='3':
        return movie_review(event,findm,question)
    elif value =='4':
        return movie_spoil(event,findm,question)
    elif value =='5':
        return  movie_detail(event,findm,question)
    elif value =='6':
        return movie_date(event,findm,question)
    elif value =='7':
        return movie_type(event,findm,question)
'''





#def filler(cut):
'''
ggg = ["ผม","อยากรู้","ว่า","ใคร","คือ","ผู้กำกับ","นะ","ครับ"]

print(filter(ggg,'0','ผมอยากรู้ว่าใครคือผู้กำกับนะครับ','wonderwoman','ผมอยากรู้ว่าใครคือผู้กำกับนะครับ'))
'''
#filter(cut,clas,event,findm,question)

'''
cut = ["ผม","อยากรู้","ว่า","ใคร","คือ","นักแสดง","นะ","ครับ"]
gg = ['แสดงนำ', 'ดาราหนัง', 'ตัวประกอบ', 'ตัวละคร', 'แสดงละคร', 'ผู้แสดง', 'แสดง', 'ดารา', 'ดาราภาพยนตร์','รับบท','การแสดง', 'นักแสดง', 'ภาพยนตร์', 'นักแสดงหลัก']
w=[]
for i in cut:
    if  i in gg:
        a='อยู่'

        w.append(a)
if w==[]:
    print('aaa')
'''
cut = ['ไปไหนมา','นักแสดง']
gg = ['แสดงนำ', 'ดาราหนัง', 'ตัวประกอบ', 'ตัวละคร', 'แสดงละคร', 'ผู้แสดง', 'แสดง', 'ดารา', 'ดาราภาพยนตร์',
      'รับบท',
      'การแสดง', 'นักแสดง', 'ภาพยนตร์', 'นักแสดงหลัก']
w = []
for i in cut:
    if i in gg:
        a = 'อยู่'
        w.append(a)

if w == []:
    text='ยังไม่มีข้อมูลนะครับ'
    print(text)

