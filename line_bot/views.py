from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from utils import message_creater
from line_bot.line_message import LineMessage



# 這是回覆使用者相同訊息

# @csrf_exempt
# def index(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         print('request:', json_data)
#         data = json_data['events'][0]
#         message = data['message']
#         reply_token = data['replyToken']
#         line_message = LineMessage(message_creater.create_single_text_message(message))
#         line_message.reply(reply_token)

#         return HttpResponse("ok")


from .models import Line_User
from accounts.models import User
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, 
    TemplateSendMessage, 
    CarouselTemplate, 
    CarouselColumn,
    PostbackAction,
    MessageAction
)
from linebot.models import TextSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent
from django.http import HttpResponse, HttpResponseBadRequest

# Line Bot API初始化
line_bot_api = LineBotApi('kOeXM+8gIjtaPPKhrVPd+sqDCsjwtcN+1dJbFQBqbEX3A2i0hVW9oDaMYb55gM1f+5wnlal1Xmp61BZTiJON6CrJsa4A5hwAuXJDe/Sr8nN8/2DHZLY3jCU3AvxwrkMnwW8vIUwDIYKhPvfnbC7kdgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fe1659d10566b01f16651411891a276c')



from django.contrib.auth import  get_user_model
User = get_user_model()



@csrf_exempt
def index(request):
    if request.method == 'POST':
        # Response headers
        signature = request.headers['X-Line-Signature']
        body = request.body.decode('utf-8')
        # print('body:',body)

        # 要先將body 轉乘python objects 才能加工
        body_json = json.loads(body)
        events = body_json.get("events", [])
        user_id = events[0]['source']['userId']
        # print('user_id:', user_id)
        
        line_user = User.objects.get(username=f"line_user_{user_id}",  password="dummy_password")
      
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse('OK', status=200)
    else:
        return HttpResponseBadRequest()


# 訊息調整
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text_message = event.message.text

    print('event', event)
    # 在這裡進行你的資料解析或其他處理
    # 例如，你可以將收到的文字訊息回傳給使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'你說:{user_id}say{text_message}')
    )


#只要解除封鎖或加入群組都會觸發這條
@handler.add(FollowEvent)
def handle_follow_event(event):
    user_id = event.source.user_id
    print(f'User {user_id} followed the bot.')

    # 開始創建line_user 綁定User
    try:
        line_user = Line_User.objects.get(line_user_id=user_id)
        print(f"Found line_user with user_id: {user_id}", line_user)

    except Line_User.DoesNotExist:
   
        # 如果找不到相應的條目，創建一個新的 User 實例
        new_user_instance = User(username=f"line_user_{user_id}", password="dummy_password")
        new_user_instance.save()

        # 使用新創建的 User 實例創建 LineUser 實例
        new_line_user = Line_User(user=new_user_instance,line_user_id= user_id)
        new_line_user.save()

        print(f"Created a new line_user with user_id: {user_id}")    
        
    # 在這裡進行追蹤事件的處理

@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    user_id = event.source.user_id
    print(event)
    print(f'User {user_id} unfollowed the bot.')
