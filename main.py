from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random
import MeCab

from wordcloud import WordCloud
from PIL import Image
import numpy as np

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
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
def handle_message(event):
    # 基本的にここにコードを書いていきます。
    # message = event.message.text
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=message))

    mecab = MeCab.Tagger()
    message = event.message.text
    result_text = mecab.parse(message)
    result_text.sub("...$","")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result_text))

    # FONT_PATH = "ipaexg.ttf"
    #####################################
    # TXT_NAME = "wakaDataSet"
    #####################################

    # def get_word_str(text):
    #     import MeCab
    #     import re
    
    #     mecab = MeCab.Tagger()
    #     parsed = mecab.parse(text)
    #     lines = parsed.split('\n')
    #     lines = lines[0:-2]
    #     word_list = []
    
    #     for line in lines:
    #         tmp = re.split('\t|,', line)
    
    #         # 名詞のみ対象
    #         if tmp[1] in ["名詞"]:
    #             # さらに絞り込み
    #             if tmp[2] in ["一般", "固有名詞"]:
    #                 word_list.append(tmp[0])
    
    #     return " " . join(word_list)
    
    #メッセージをテキストファイルに追加
    # post_text = event.message.text
    # with open(TXT_NAME + ".txt", mode='a' , encoding="utf8") as f:
    #     f.write("," + post_text)


    # テキストファイル読み込み
    # read_text = open(TXT_NAME + ".txt", encoding="utf8").read()

    ####################################################
    # マスクを作成する
    # mask_array = np.array(Image.open('tree080948.png'))
    #####################################################

    # 文字列取得
    # word_str = get_word_str(read_text)
    
    # 画像作成
    # wc = WordCloud(font_path=FONT_PATH, mask=mask_array, background_color='white', colormap='bone', contour_width=3).generate(word_str)
    
    # 画像保存（テキストファイル名で）
    # wc.to_file(TXT_NAME + ".png")

    # PILで表示する
    # image_array = wc.to_array()
    # img = Image.fromarray(image_array)
    # img.to_file("/static/images" + TXT_NAME + ".png")


    # line_bot_api.reply_message(
    # event.reply_token,
    # TextSendMessage(text=mecab.parse(post_text)))

        


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
