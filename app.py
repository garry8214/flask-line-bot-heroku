# https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-echo/app_with_handler.py
 
 import os
 import sys
 from argparse import ArgumentParser
 
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
 
 # get channel_secret and channel_access_token from your environment variable
 channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
 channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
 if channel_secret is None:
     print('Specify LINE_CHANNEL_SECRET as environment variable.')
     sys.exit(1)
 if channel_access_token is None:
     print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
     sys.exit(1)
 
 line_bot_api = LineBotApi(channel_access_token)
 handler = WebhookHandler(channel_secret)
 
 
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
 def message_text(event):
     user_id = event.source.user_id
     print('user_id:' + user_id)
     line_bot_api.reply_message(
         event.reply_token,
         #TextSendMessage(text=user_id + event.message.text)
         TextSendMessage(text="Gary:" + event.message.text)
     )
 
 
 if __name__ == "__main__":
     arg_parser = ArgumentParser(
         usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
     )
     arg_parser.add_argument('-p', '--port', default=8000, help='port')
     arg_parser.add_argument('-d', '--debug', default=False, help='debug')
     options = arg_parser.parse_args()
 
     app.run(debug=options.debug, port=options.port)
