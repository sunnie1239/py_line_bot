from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ZR8t5vCcdxxyLX0hIB2iCtR5Uj5RW1oQtAud99eGXtc8p2ejGOdYZISt1tfhKq2CTPXafGlLB9dX8F8lAcivHiW37ah8P2z6aqrlAMg7xnnlcrAGS56ofIL3gPZB6wOYCiAiVv5Ash9gceNpV7PApwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('90c838f698c3ae780c1d2325abc49868')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()