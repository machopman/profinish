import difflib
import random

from actor import movie_actor
from date import movie_date
from detail import movie_detail
from director import movie_director
from enjoy import movie_enjoy
from image import movie_image
#from googletrans import Translator
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
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImagemapSendMessage, BaseSize,
                            URIImagemapAction, ImagemapArea, MessageImagemapAction, TemplateSendMessage,
                            CarouselTemplate, CarouselColumn, MessageTemplateAction, URITemplateAction,
                            PostbackTemplateAction)
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
    question = event
    question = checkd(question)

    sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', question).replace(' ', '')
    print(sentence)
    if sentence !='':
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
            print(p)
            classify = p
            user = mongo.db.users

            userid = event.source.user_id

            name = re.sub('[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฝฦใฬมฒท?ื์ิ.่๋้็เโ,ฯี๊ัํะำไๆ๙๘๗๖๕ึ฿ุู๔๓๒๑+ๅาแ]',
                          '',
                          question).replace(' ', '')
            movie_name = searchMovieNameInDic(question)


            if  (name == '') and (movie_name == '') and classify == 9:
                general(question, event, userid, user)
            else:
                Type(classify, event, movie_name, userid, user, question, name)

def Type(q, event, movie_name,userid,user,question,name):
    if q == 0: #actor
        if name != '' and q != 9 and q != 8:
            detail = movie_actor(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_actor(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_actor(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        if (name =='')and (movie_name!='') :
            user.insert(
                {"UserId": userid, "NameMovie": movie_name, "Cate": 'Actor', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": 'Actor', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name != '') and (name != ''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": 'Actor', "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        else:
            user.insert(
                {"UserId": userid, "NameMovie": findmovie(userid), "Cate": 'Actor', "Question": question, "Answer": detail,
                 "Time": datetime.now()})

    if q == 1:#"director"


        if name != '' and q != 9 and q != 8:
            detail = movie_director(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_director(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_director(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))
        if (name =='')and (movie_name!=''):
            user.insert(
                {"UserId": userid, "NameMovie": movie_name, "Cate": "director", "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": "director", "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        elif (movie_name != '') and (name != ''):
            user.insert(
                {"UserId": userid, "NameMovie": name, "Cate": "director", "Question": question, "Answer": detail,
                 "Time": datetime.now()})
        else:
            user.insert(
                {"UserId": userid, "NameMovie": findmovie(userid), "Cate": "director", "Question": question, "Answer": detail,
                 "Time": datetime.now()})

    if q == 2:#"image"
        if name != '' and q != 9 and q != 8:
            detail = movie_image(event,question,userid)
            image_message = ImageSendMessage(
                original_content_url=detail,
                preview_image_url=detail
            )
            line_bot_api.push_message(userid,image_message)

        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_image(event,question,userid)
            image_message = ImageSendMessage(
                original_content_url=detail,
                preview_image_url=detail
            )
            line_bot_api.push_message(userid, image_message)

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_image(event,question,userid)
            image_message = ImageSendMessage(
                original_content_url=detail,
                preview_image_url=detail
            )
            line_bot_api.push_message(userid, image_message)

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "image", "Question": question,
                         "Answer": 'รูปภาพ'+movie_name, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "image", "Question": question,
                         "Answer": 'รูปภาพ'+name, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "image", "Question": question,
                         "Answer": 'รูปภาพ'+movie_name, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie":findmovie(userid), "Cate": "image", "Question": question,
                         "Answer": 'รูปภาพ'+findmovie(userid), "Time": datetime.now()})
    if q == 3:#"review"
        if name != '' and q != 9 and q != 8:
            detail = movie_review(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_review(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_review(event,question,userid)
            if detail!= 'เรื่องอะไรครับ' or detail != 'เรื่องอะไรนะครับ':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))


        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "review", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "review", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "review", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie":findmovie(userid), "Cate": "review", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
    if q == 4: #"spoil"
        if name != '' and q != 9 and q != 8:
            detail = movie_spoil(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_spoil(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_spoil(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "spoil", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "spoil", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "spoil", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie":findmovie(userid), "Cate": "spoil", "Question": question,
                         "Answer": detail, "Time": datetime.now()})

    if q == 5: #"detail"
        if name != '' and q != 9 and q != 8:
            detail = movie_detail(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_detail(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_detail(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "detail", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "detail", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "detail", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": "detail", "Question": question,
                         "Answer": detail, "Time": datetime.now()})

    if q == 6: #"date"

        if name != '' and q != 9 and q != 8:
            detail = movie_date(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_date(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_date(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!=''):
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "date", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "date", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name !='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "date", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": "date", "Question": question,
                         "Answer": detail, "Time": datetime.now()})

    if q == 7: #"type"
        if name != '' and q != 9 and q != 8:
            detail = movie_type(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name != '') and q != 9 and q != 8:
            detail = movie_type(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        elif (name == '') and (movie_name == '') and q != 9 and q != 8:
            detail = movie_type(event,question,userid)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

        if (name =='')and (movie_name!='') :
            user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "type", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name =='')and(name !=''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "type", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        elif (movie_name != '') and (name != ''):
            user.insert({"UserId": userid, "NameMovie": name, "Cate": "type", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
        else:
            user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": "type", "Question": question,
                         "Answer": detail, "Time": datetime.now()})
    if q == 8:
        if 'สนุก' in question:
            if name != '' and q != 9 :
                detail = movie_enjoy(event,question,userid)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

            elif (name == '') and (movie_name != '') and q != 9 :
                detail = movie_enjoy(event,question,userid)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

            elif (name == '') and (movie_name == '') and q != 9 :
                detail = movie_enjoy(event,question,userid)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detail))

            if (name =='')and (movie_name!='') :
                user.insert({"UserId": userid, "NameMovie": movie_name, "Cate": "type", "Question": question,
                             "Answer": detail, "Time": datetime.now()})
            elif (movie_name =='')and(name !=''):
                user.insert({"UserId": userid, "NameMovie": name, "Cate": "type", "Question": question,
                             "Answer": detail, "Time": datetime.now()})
            elif (movie_name != '') and (name != ''):
                user.insert({"UserId": userid, "NameMovie": name, "Cate": "type", "Question": question,
                             "Answer": detail, "Time": datetime.now()})
            else:
                user.insert({"UserId": userid, "NameMovie": findmovie(userid), "Cate": "type", "Question": question,
                             "Answer": detail, "Time": datetime.now()})
        elif 'แนะนำหนัง' in question:

            message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=searchpic(),
                            title='this is menu1',
                            text='description1',
                            actions=[
                                PostbackTemplateAction(
                                    label='postback1',
                                    text='postback text1',
                                    data='action=buy&itemid=1'
                                ),
                                MessageTemplateAction(
                                    label='message1',
                                    text='message text1'
                                ),
                                URITemplateAction(
                                    label='uri1',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=searchpic(),
                            title='this is menu2',
                            text='description2',
                            actions=[
                                PostbackTemplateAction(
                                    label='postback2',
                                    text='postback text2',
                                    data='action=buy&itemid=2'
                                ),
                                MessageTemplateAction(
                                    label='message2',
                                    text='message text2'
                                ),
                                URITemplateAction(
                                    label='uri2',
                                    uri='http://mandm.plearnjai.com/'
                                )
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
            return 0



def  checkd(question):
     name = searchMovieNameInDic(question)
     sentence = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '', question).replace(' ', '')
     if sentence!='':
         if sentence !='' or name !='':
             if name in question:
                 u = question.replace(name,'')
                 return u
             if name not in question:
                 return sentence
         if sentence =='' and name =='':
              return  question
     elif sentence=='':
         return question


def searchMovieNameInDic(question):
    cut = cutw(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = json.load(f)
        e = ''
        for key, value in a.items():
            for i in cut:
                if i in value:
                    w = key.lower()
                    u  =str(w)
                    e = e+u
        return e

def checDic(question):
    cut = cutw(question)
    with open('new.txt', mode='r', encoding='utf-8-sig') as f:
        a = json.load(f)
        e = ''
        for key, value in a.items():
            for i in cut:
                if i in value:
                    w = i
                    u  =str(w)
                    e = e+u
        return e

def general(question, event,userid,user):
    if question.find('สบายดี') >= 0:
        text = 'สบายดีครับ'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('สวัส') >= 0:
        text = 'สวัสดีจ้า'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('บายดี') >= 0:
        text = 'สบายดีจร้า'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('กำลังทำ') >= 0:
        text = 'กำลังรีวิวหนังอยู่ครับ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('ได้ไหม') >= 0:
        text = 'ได้สิ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('ขอบคุณ') >= 0:
        text = 'ยินดีจร้า'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('ลาก่อน') >= 0:
        text = 'จร้าไว้คุยกันอีกนะ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('ชื่อไร') >= 0:
        text = 'ผมชื่อมูวี่จัง'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question.find('ทำอะไร') >= 0:
        text = 'กำลังพูดคุยกับคุณอยู่ครับ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'ไปไหน' in question:
        text = 'ไปหาข้อมูลมารีวิวหนังแปบนึงนะ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'รู้จัก' in question:
        text = 'รู้จักสิแฟนเราเอง'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'แฟนเราเอง' in question:
        text = 'ไม่สิอย่ามโน'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'แง' in question:
        text = 'พูดไม่เพราะเลยนะครับ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'ป่าวนะ' in question:
        text = 'ไม่เชื่อ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif '555' in question:
        text = 'หัวเราะๆๆ'
        print(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'อยากมีแฟน' in question:
        text = 'หาสิ้ๆๆ'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif 'อยาก' in question:
        text = 'อยากอะไรฮะ'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    elif question == 'หาให้หน่อย':
        text = 'จะให้เราแฟนให้อะดิ'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})
    else:
        text = 'ไม่รู้ครับ'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text,'time':datetime.now()})


'''
    a = ["ทำอะไรได้บ้าง","การทำงาน","มีความสามารถไรบ้าง","ทำไรได้","สามารถทำอะไรได้","ความสามารถของบอท","มีฟังชันอะไรบ้าง","ฟังชั่นอะไร","ความสามารถพิเศษ"]
    b = ["สวัสดี", "ดีจ้า", "สวัสดีค่ะ", "สวัสดีครับ", "สวัส", "ดีจร้า", "ดีงับ", "สวัดดี", 'สวัสดีตอนบ่าย','สวัสดีตอนเย็น']
    z = difflib.get_close_matches(question, a)
    y = difflib.get_close_matches(question, b)
    if z[0] in a:
        text = checkfunction(event, userid)
        ans = ''
        for i in text:
            ans = ans+i
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ans))
        user.insert({'userid': userid, 'question': question, 'answer': ans, 'time': datetime.now()})
    if  y[0] in b:
        ans = ['สวัสดีจร้า','สวัสดีค่ะ','ดีจ้า','สวัสดี']
        text = random.choice(ans)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        user.insert({'userid': userid, 'question': question, 'answer': text, 'time': datetime.now()})
'''




if __name__ == "__main__":
    app.run()