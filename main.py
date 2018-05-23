import difflib

from classifyname import checDic
from normalize import normalword
import random
from checkName import checkname
from actor import movie_actor
from date import movie_date
from detail import movie_detail
from director import movie_director
from enjoy import movie_enjoy
from image import movie_image
from namemoviebefore  import findmovie
from searchpic import searchpic
import json
import numpy as np
import tensorflow as tf
from cutword import cutw
from checkdic import checkd
from searchMovieNameInDic import searchMovieNameInDic
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage,
                            CarouselTemplate, CarouselColumn, MessageTemplateAction, URITemplateAction)
import re
from flask.ext.pymongo import PyMongo
from review import movie_review
from spoil import movie_spoil
from type import movie_type
from datetime import datetime

app = Flask(__name__)

line_bot_api = LineBotApi(
    'iYDoDLW1k4yIYJvMnHVi18Vhl0NXPh5ec6a4FLdlR/en3nqmGCWsF/QeYKX8MPj2DYUFbjsEos/+HGUA7LgF4OimIUh1WD9j/phhG/vqX9zZD92iiw/t+kpE1AadWCIdwkzMuxEvAbCM84LtdTkQSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('935cecc6bf121cf08c1cea288956462b')
app.config['MONGO_DBNAME'] = 'moviebot'
app.config['MONGO_URI'] = 'mongodb://pretty:shop1234@ds139942.mlab.com:39942/moviebot'
mongo = PyMongo(app)

reverse_dictionary = json.load(open("reverse_dictionaryCNNnew.txt"))
final_embeddings = np.loadtxt('final_embeddingsCNNnew.txt')
dictionary = {v: int(k) for k, v in reverse_dictionary.items()}




@app.route("/")
def hello():
    return "Hello World!"


@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def movie(event):
    user = mongo.db.users
    q = event.message.text
    question= normalword(q)
    chec = checDic(question)
    ques = checkd(question)
    userid = event.source.user_id
    findm =findmovie(userid)

    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', ques).replace(' ', '')

    if sentence !='' :
        cut = cutw(sentence)
        print(cut)

        words = []
        for row in cut:
            words.append(row)
        max = 15
        word = ''
        for line in words:
            cut_len = len(line) - 1
            # print(cut)
            if cut_len >= max:
                max = cut_len

        cut_len = len(cut)
        count1 = max - cut_len
        # word = []
        for line2 in range(count1):
            str = 'PAD'
            words.append(str)
        inputs = {'input': [words], 'cate': [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]}
        inputs2 = []
        for poemCount in range(len(inputs['input'])):
            poem = []
            for count in range(15):
                search = inputs['input'][poemCount][count]
                search = search.replace('\ufeff', '')

                if search != 'PAD':
                    # print(search)
                        index = dictionary[search]
                        # [i for i, word in reverse_dictionary.items() if word == search]
                        if index != None:

                            # print(index)
                            poem = np.concatenate((poem, final_embeddings[index]))
                            # print(poem.shape)
                        else:
                            print(search)
                            # print(poem)

                else:
                    poem = np.concatenate((poem, np.zeros(22)))
            inputs2.append(poem)
        graph = tf.Graph()
        with graph.as_default():
            wordCount = 15
            cateDimension = 10
            weightColumn1 = 22
            weightColumn2 = 64
            weightRow = 3
            features1 = 64
            features2 = 64

            sess = tf.InteractiveSession()
            pooled_outputs = []
            x = tf.placeholder(tf.float32, shape=[None, wordCount * weightColumn1])
            y_ = tf.placeholder(tf.float32, shape=[None, cateDimension])
            # y_ = tf.placeholder(tf.float32, shape=[None, cateDimension])
            for i, filter_size in enumerate([2, 3, 4]):
                l2_loss = tf.constant(0.0)
                l2_reg_lambda = 0.0
                with tf.name_scope("conv-maxpool-%s" % filter_size):
                    # Convolution Layer
                    filter_shape = [filter_size, weightColumn1, 1, features1]
                    W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                    b = tf.Variable(tf.constant(0.1, shape=[features1]), name="b")

                    # print(x.get_shape())
                    # print(W.get_shape())
                    x_image = tf.reshape(x, [-1, wordCount, weightColumn1, 1])
                    conv = tf.nn.conv2d(x_image, W, strides=[1, 1, 1, 1], padding='VALID')

                    # Apply nonlinearity

                    h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                    # Maxpooling over the outputs
                    pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, 15 - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding='VALID',
                        name="pool")
                    pooled_outputs.append(pooled)

            # Combine all the pooled features
            num_filters_total = features1 * len([2, 3, 4])
            print(pooled_outputs)

            # h_pool = tf.concat(3, pooled_outputs)
            h_pool = tf.concat(pooled_outputs, 3)
            h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])

            # Add dropout
            with tf.name_scope("dropout"):
                keep_prob = tf.placeholder(tf.float32)

                h_drop = tf.nn.dropout(h_pool_flat, keep_prob)

            # Final (unnormalized) scores and predictions
            with tf.name_scope("output"):
                W = tf.get_variable(
                    "W",
                    shape=[num_filters_total, cateDimension],
                    initializer=tf.contrib.layers.xavier_initializer())
                b = tf.Variable(tf.constant(0.1, shape=[cateDimension]), name="b")
                l2_loss += tf.nn.l2_loss(W)
                l2_loss += tf.nn.l2_loss(b)
                # scores = tf.nn.xw_plus_b(h_drop, W, b, name="scores")
                scores = tf.nn.relu(tf.nn.xw_plus_b(h_drop, W, b, name="scores"))
                # predictions = tf.argmax(scores, 1, name="predictions")

            # CalculateMean cross-entropy loss
            with tf.name_scope("loss"):
                losses = tf.nn.softmax_cross_entropy_with_logits(logits=scores, labels=y_)
                loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

            correct_prediction = tf.equal(tf.argmax(scores, 1), tf.argmax(y_, 1))
            train_step = tf.train.AdamOptimizer(1e-4).minimize(losses)  #######///
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  ########///

            saver = tf.train.Saver()  # Gets all variables in `graph`.
            with tf.Session(graph=graph) as sess:
                saver.restore(sess, 'model.ckpt')
                p = sess.run(tf.argmax(scores, 1), feed_dict={x: inputs2, keep_prob: 1.0})

            classify = p
            clas = checkcate(classify)
            print(classify)

            name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]','', question).replace(' ', '')
            movie_name = searchMovieNameInDic(question)


            if findm == '' and classify!=9 and classify!=8 and name =='':
                if chec == '':
                    text = 'เรื่องอะไรครับ'
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
                    user.insert(
                        {"UserId": userid, "NameMovie": "", "Cate": clas, "Question": question, "Answer": text,"Time": datetime.now()})

            elif (name == '') and (movie_name == '') and classify == 9:
                general(question, event, userid, user)
            else:
                Type(clas, event, movie_name, userid, user, question, name,findm)

    elif findm == '':
        check = checkname(question)

        if chec != '' or check==True:
            movie_name =''
            w = user.find({'UserId':userid}).sort("Time")
            q = []
            t=[]
            for i in w:
                a = i
                for key, value in a.items():
                    if key == 'Question':
                        q.append(value)
                    if key =='Cate':
                        t.append(value)


            ques = q[-1]+chec
            Type(t[-1], event, movie_name, userid, user, ques, chec,findm)
        elif chec=='':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='กรุณาพิมพ์ชื่อหนังให้ถูกด้วย'))




def Type(q, event, movie_name,userid,user,question,name,findm):
    print('ประเภท'+"="+q)
    print('ชื่อหนังพบในdic'+"="+movie_name)
    print('คำถาม'+"="+question)
    print('ชื่อหนัง'+"="+name)
    print('ชื่อหนังก่อนหน้า'+"="+name)

    if q == '0': #actor
        if 'แสดง' not in question:
            p = ['เทส', 'ยังไม่รู้เลยจร้า', 'ไม่รู้เหมือนกัน', 'น่าจะเป็นอย่างนั้น', 'ขอไปหาข้อมูลแปบ',
                 'ขอไปศึกษาก่อนเดี๋ยวมาตอบ', 'ไว้วันหลังจะมาตอบ', 'คลาวหน้าจะมาตอบนะ']
            text = random.choice(p)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        elif name != '' :
            detail = movie_actor(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name != '') :
            detail = movie_actor(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name == ''):
            detail = movie_actor(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!='') :
            user.insert(
                {"UserId": userid, "NameMovie": movie_name, "Cate": '0', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": '0', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name != '') and (name != ''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": '0', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        else:
            user.insert(
                {"UserId": userid, "NameMovie": findmovie(userid), "Cate": '0', "Question": question, "Answer": detail,
                 "Time": datetime.now()})

    if q == '1':#"director"
        if 'กำกับ' not in question:
            p = ['เทส', 'ยังไม่รู้เลยจร้า', 'ไม่รู้เหมือนกัน', 'น่าจะเป็นอย่างนั้น', 'ขอไปหาข้อมูลแปบ',
                 'ขอไปศึกษาก่อนเดี๋ยวมาตอบ', 'ไว้วันหลังจะมาตอบ', 'คลาวหน้าจะมาตอบนะ']
            text = random.choice(p)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        elif name != '' :
            detail = movie_director(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name != ''):
            detail = movie_director(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name == '') :
            detail = movie_director(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        if (name =='')and (movie_name!=''):
            user.insert(
                {"UserId": userid, "NameMovie": movie_name, "Cate": '1', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": '1', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name != '') and (name != ''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": '1', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        else:
            user.insert(
                {"UserId": userid, "NameMovie": findmovie(userid), "Cate": '1', "Question": question, "Answer": detail,
                 "Time": datetime.now()})

    if q == '2':#"image"

        if name != '' :
            detail = movie_image(event,findm,question)
            image_message = ImageSendMessage(
                original_content_url=detail,
                preview_image_url=detail
            )
            line_bot_api.push_message(userid,image_message)

        elif (name == '') and (movie_name != '') :
            detail = movie_image(event,findm,question)
            image_message = ImageSendMessage(
                original_content_url=detail,
                preview_image_url=detail
            )
            line_bot_api.push_message(userid, image_message)

        elif (name == '') and (movie_name == '') :
            detail = movie_image(event,findm,question)
            image_message = ImageSendMessage(
                original_content_url=detail,
                preview_image_url=detail
            )
            line_bot_api.push_message(userid, image_message)

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '2', "Question": question,
                         "Answer": 'รูปภาพ'+movie_name, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '2', "Question": question,
                         "Answer": 'รูปภาพ'+name, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '2', "Question": question,
                         "Answer": 'รูปภาพ'+movie_name, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie":findmovie(userid), "Cate": '2', "Question": question,
                         "Answer": 'รูปภาพ'+findmovie(userid), "Time": datetime.now()})
    if q == '3':#"review"
        if name != '':
            detail = movie_review(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') :
            detail = movie_review(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') :
            detail = movie_review(event,findm,question)
            if detail!= 'เรื่องอะไรครับ' or detail != 'เรื่องอะไรนะครับ':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))


        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '3', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '3', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '3', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie":findmovie(userid), '3': "review", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
    if q == '4': #"spoil"
        if name != '' :
            detail = movie_spoil(event, question, userid)
            print(detail)

            if len(detail) > 1999 and len(detail) < 4000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[0:1998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[1999:]))
            elif len(detail) >= 4000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[0:1998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[1999:3998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[3999:]))
            elif len(detail) < 2000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') :
            detail = movie_spoil(event, question, userid)
            if len(detail) > 1999 and len(detail) < 4000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[0:1998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[1999:]))
            elif len(detail) >= 4000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[0:1998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[1999:3998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[3999:]))
            elif len(detail) < 2000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_spoil(event, question, userid)
            if len(detail) > 1999 and len(detail) < 4000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[0:1998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[1999:]))
            elif len(detail) >= 4000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[0:1998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[1999:3998]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail[3999:]))
            elif len(detail) < 2000:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '4', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '4', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '4', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie":findmovie(userid), "Cate": '4', "Question": question,
                         "Answer": detail, "Time": datetime.now()})

    if q == '5': #"detail"
        if name != '':
            detail = movie_detail(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') :
            detail = movie_detail(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') :
            detail = movie_detail(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '5', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '5', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '5', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": '5', "Question": question,
                         "Answer": detail, "Time": datetime.now()})

    if q == '6': #"date"

        if name != '' :
            detail = movie_date(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') :
            detail = movie_date(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') :
            detail = movie_date(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '6', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '6', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '6', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate":'6', "Question": question,
                         "Answer": detail, "Time": datetime.now()})

    if q == '7': #"type"
        if name != '' :
            detail = movie_type(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') :
            detail = movie_type(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') :
            detail = movie_type(event,findm,question)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!='') :
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '7', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '7', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name != '') and (name != ''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": '7', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": '7', "Question": question,
                         "Answer": detail, "Time": datetime.now()})
    if q == '8':
        a = ["ทำอะไรได้บ้าง", "การทำงาน", "มีความสามารถไรบ้าง", "ทำไรได้", "สามารถทำอะไรได้", "ความสามารถของบอท",
             "มีฟังชันอะไรบ้าง", "ฟังชั่นอะไร", "ความสามารถพิเศษ", 'ถามอะไรได้บ้าง', 'สามารถทำอะไรได้']
        z = difflib.get_close_matches(question, a)
        if 'สนุก' in question:
            if name != '' and q != 9 :
                detail = movie_enjoy(event,findm,question)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

            elif (name == '') and (movie_name != '') and q != '9' :
                detail = movie_enjoy(event,findm,question)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

            elif (name == '') and (movie_name == '') and q != '9' :
                detail = movie_enjoy(event,findm,question)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

            if (name =='')and (movie_name!='') :
                user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": '8', "Question": question,
                             "Answer": detail, "Time": datetime.now()})
            elif (movie_name =='')and(name !=''):
                user.insert({"UserId": userid, "NameMovie": name, "Cate": '8', "Question": question,
                             "Answer": detail, "Time": datetime.now()})
            elif (movie_name != '') and (name != ''):
                user.insert({"UserId": userid, "NameMovie": name, "Cate": '8', "Question": question,
                             "Answer": detail, "Time": datetime.now()})
            else:
                user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": '8', "Question": question,
                             "Answer": detail, "Time": datetime.now()})
        elif 'แนะนำหนัง' in question:
            a = []
            d =[]
            f = []
            for i in range(6):
                b = searchpic()[0]
                a.append(b)
                c = searchpic()[1]
                d.append(c)
                e = searchpic()[2]
                f.append(e)


            message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=a[0],
                            title=d[0],
                            text=f[0],
                            actions=[
                                MessageTemplateAction(
                                    label='เรื่องย่อ',
                                    text='เรื่องย่อ'
                                ),
                                MessageTemplateAction(
                                    label='บทรีวิว',
                                    text='บทรีวิว'
                                ),
                                URITemplateAction(
                                    label='website',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=a[1],
                            title=d[1],
                            text=f[1],
                            actions=[
                                MessageTemplateAction(
                                    label='เรื่องย่อ',
                                    text='เรื่องย่อ'
                                ),
                                MessageTemplateAction(
                                    label='บทรีวิว',
                                    text='บทรีวิว'
                                ),
                                URITemplateAction(
                                    label='website',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=a[2],
                            title=d[2],
                            text=f[2],
                            actions=[
                                MessageTemplateAction(
                                    label='เรื่องย่อ',
                                    text='เรื่องย่อ'
                                ),
                                MessageTemplateAction(
                                    label='บทรีวิว',
                                    text='บทรีวิว'
                                ),
                                URITemplateAction(
                                    label='website',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=a[3],
                            title=d[3],
                            text=f[3],
                            actions=[
                                MessageTemplateAction(
                                    label='เรื่องย่อ',
                                    text='เรื่องย่อ'
                                ),
                                MessageTemplateAction(
                                    label='บทรีวิว',
                                    text='บทรีวิว'
                                ),
                                URITemplateAction(
                                    label='website',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=a[4],
                            title=d[4],
                            text=f[4],
                            actions=[
                                MessageTemplateAction(
                                    label='เรื่องย่อ',
                                    text='เรื่องย่อ'
                                ),
                                MessageTemplateAction(
                                    label='บทรีวิว',
                                    text='บทรีวิว'
                                ),
                                URITemplateAction(
                                    label='website',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=a[5],
                            title=d[5],
                            text=f[5],
                            actions=[
                                MessageTemplateAction(
                                    label='เรื่องย่อ',
                                    text='เรื่องย่อ'
                                ),
                                MessageTemplateAction(
                                    label='บทรีวิว',
                                    text='บทรีวิว'
                                ),
                                URITemplateAction(
                                    label='website',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
            return 0

        elif z[0] in a:
            message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title='สามารถถามได้ดังนี้',
                            text='ถามเกี่ยวกับ',
                            actions=[

                                MessageTemplateAction(
                                    label='นักแสดง',
                                    text='ใครเป็นนักแสดง wonderwoman'
                                ),
                                MessageTemplateAction(
                                    label='ผู้กำกับ',
                                    text='ใครเป็นผู้กำกับวันเดอวูแมน'
                                ),
                                MessageTemplateAction(
                                    label='รูปภาพ',
                                    text='อยากดูรูปภาพwonderwoman'
                                )

                            ]
                        ),
                        CarouselColumn(
                            title='สามารถถามได้ดังนี้',
                            text='ถามเกี่ยวกับ',
                            actions=[

                                MessageTemplateAction(
                                    label='รีวิว',
                                    text='อยากอ่านรีวิวwonderwoman'
                                ),
                                MessageTemplateAction(
                                    label='สปอย',
                                    text='อยากดูสปอยwonderwoman'
                                ),
                                MessageTemplateAction(
                                    label='เรื่องย่อภาพยนตร์',
                                    text='อยากอ่านเรื่องย่อwonderwoman'
                                )
                            ]
                        ),
                        CarouselColumn(
                            title='สามารถถามได้ดังนี้',
                            text='ถามเกี่ยวกับ',
                            actions=[

                                MessageTemplateAction(
                                    label='ประเภทหนัง',
                                    text='wonderwonเป็นหนังประเภทอะไร'
                                ),
                                MessageTemplateAction(
                                    label='วันฉายภาพยนตร์',
                                    text='wonderwomanฉายวันไหน'
                                ),
                                MessageTemplateAction(
                                    label='ความสนุก',
                                    text='wonderwomanสนุกไหม'
                                )
                            ]
                        ),
                        CarouselColumn(
                            title='สามารถถามได้ดังนี้',
                            text='ถามเกี่ยวกับ',
                            actions=[

                                MessageTemplateAction(
                                    label='แนะนำภาพยนตร์',
                                    text='แนะนำหนังหน่อย'
                                ),
                                MessageTemplateAction(
                                    label='การทักทายทั่วไป',
                                    text='สบายดีไหม'
                                ),
                                MessageTemplateAction(
                                    label='-',
                                    text='-'
                                )

                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        else:
            p =['คืออย่างที่คุณคิดเลย','ยังไม่รู้เลยจร้า','ไม่รู้เหมือนกัน','น่าจะเป็นอย่างนั้น','ขอไปหาข้อมูลแปบ','ขอไปศึกษาก่อนเดี๋ยวมาตอบ','ไว้วันหลังจะมาตอบ','คลาวหน้าจะมาตอบนะ']
            text= random.choice(p)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": '8', "Question": question,
                         "Answer": text, "Time": datetime.now()})



def checkcate(classify):
    if classify ==0:
        return '0'
    elif classify == 1:
        return  '1'
    elif classify ==2:
        return '2'
    elif classify ==3:
        return '3'
    elif classify ==4:
        return '4'
    elif classify ==5:
        return '5'
    elif classify ==6:
        return '6'
    elif classify ==7:
        return '7'
    elif classify==8:
        return '8'

def general(question, event,userid,user):
   try:
       b = ["สวัสดี", "ดีจ้า", "สวัสดีค่ะ", "สวัสดีครับ", "สวัส", "ดีงับ", "สวัดดี", 'สวัสดีตอนบ่าย','สวัสดีตอนเย็น']
       y = difflib.get_close_matches(question, b)
       if  y[0] in b:
            ans = ['สวัสดีจร้า','สวัสดีค่ะ','ดีจ้า','สวัสดี']
            text = random.choice(ans)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            #user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
   except:

       if question.find('สบายดี') >= 0:
           text = 'สบายดีครับ'
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})

       elif question.find('บายดี') >= 0:
           text = 'สบายดีจร้า'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question.find('กำลังทำ') >= 0:
           text = 'กำลังรีวิวหนังอยู่ครับ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question.find('ได้ไหม') >= 0:
           text = 'ได้สิ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question.find('ขอบคุณ') >= 0:
           text = 'ยินดีจร้า'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question.find('ลาก่อน') >= 0:
           text = 'จร้าไว้คุยกันอีกนะ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question.find('ชื่อไร') >= 0:
           text = 'ผมชื่อมูวี่จัง'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question.find('ทำอะไร') >= 0:
           text = 'กำลังพูดคุยกับคุณอยู่ครับ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'ไปไหน' in question:
           text = 'ไปหาข้อมูลมารีวิวหนังแปบนึงนะ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'รู้จัก' in question:
           text = 'รู้จักสิแฟนเราเอง'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'แฟนเราเอง' in question:
           text = 'ไม่สิอย่ามโน'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'แง' in question:
           text = 'พูดไม่เพราะเลยนะครับ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'ป่าวนะ' in question:
           text = 'ไม่เชื่อ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif '555' in question:
           text = 'หัวเราะๆๆ'
           print(text)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'อยากมีแฟน' in question:
           text = 'หาสิ้ๆๆ'
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif 'อยาก' in question:
           text = 'อยากอะไรฮะ'
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       elif question == 'หาให้หน่อย':
           text = 'จะให้เราแฟนให้อะดิ'
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
       else:
           p = ['คืออย่างที่คุณคิดเลย', 'ยังไม่รู้เลยจร้า', 'ไม่รู้เหมือนกัน', 'น่าจะเป็นอย่างนั้น', 'ขอไปหาข้อมูลแปบ',
                'ขอไปศึกษาก่อนเดี๋ยวมาตอบ', 'ไว้วันหลังจะมาตอบ', 'คลาวหน้าจะมาตอบนะ']
           text = random.choice(p)
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
           user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})



if __name__ == "__main__":
    app.run()
