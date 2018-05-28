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
from searchMovieNameInDic import  searchMovie
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
from key import diffli
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
    f= event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f))




if __name__ == "__main__":
    app.run()
