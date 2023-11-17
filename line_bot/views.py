from django.shortcuts import render, get_object_or_404
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
    MessageAction,
    QuickReply, 
    QuickReplyButton,
    FlexSendMessage, BubbleContainer, BoxComponent, TextComponent
)
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
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse('OK', status=200)
    else:
        return HttpResponseBadRequest()

from financial_records.models import Category,FinancialRecord
from groups.models import Groups 

def handle_command(event, user_id, command):
    parts = command.split()

    if len(parts) < 3:
        return "指令格式不正確。使用：/b 100 一支筆 [描述] 或 /c 50000 收入 [描述]"

    amount = parts[1]
    record_name = parts[2]
    description = " ".join(parts[3:]) if len(parts) > 3 else None

    currency_index = parts.index('幣值') if '幣值' in parts else -1
    currency = parts[currency_index + 1] if currency_index != -1 and len(parts) > currency_index + 1 else 1


    user = get_object_or_404(User, username=f"line_user_{user_id}")
    print(user)

    group, created = Groups.objects.get_or_create(group_name="損益表（line自動創建)", created_by=user)
 
    category, created = Category.objects.get_or_create(group=group, name="支出(由line自動創建)",created_by=user)
   
 
    record = FinancialRecord.objects.create(
        group=group,
        name=record_name,
        description=description,
        debit=amount,
        currency=currency,
        created_by=user
    )
    record.category.add(category) 
    return f"已创建支出记录：{record_name}，金额：{amount}，描述，剩下餘額：{record.balance}"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    command = event.message.text

    # 处理指令
    response = handle_command(event, user_id, command)

    # 回复用户
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))


# 表格範例

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_id = event.source.user_id
#     text_message = event.message.text

#     # 构建表格的数据
#     table_data = [
#         {"name": "John", "age": 25, "city": "New York"},
#         {"name": "Alice", "age": 28, "city": "San Francisco"},
#         {"name": "Bob", "age": 22, "city": "Los Angeles"},
#     ]

#     # 创建 Flex Message 中的 BubbleContainer
#     bubble = BubbleContainer(
#         body=BoxComponent(
#             layout="vertical",
#             contents=[
#                 TextComponent(text="Table", weight="bold", size="xl"),
#                 BoxComponent(
#                     layout="vertical",
#                     margin="lg",
#                     spacing="sm",
#                     contents=[
#                         BoxComponent(
#                             layout="horizontal",
#                             spacing="sm",
#                             contents=[
#                                 TextComponent(text="Name", color="#aaaaaa", size="sm", flex=2),
#                                 TextComponent(text="Age", color="#aaaaaa", size="sm", flex=1),
#                                 TextComponent(text="City", color="#aaaaaa", size="sm", flex=2),
#                             ],
#                         )
#                     ] +
#                     [
#                         BoxComponent(
#                             layout="horizontal",
#                             spacing="sm",
#                             contents=[
#                                 TextComponent(text=f"{data['name']}", size="sm", flex=2),
#                                 TextComponent(text=f"{data['age']}", size="sm", flex=1),
#                                 TextComponent(text=f"{data['city']}", size="sm", flex=2),
#                             ],
#                         )
#                         for data in table_data
#                     ],
#                 ),
#             ],
#         ),
#     )

#     # 创建 Flex Message
#     flex_message = FlexSendMessage(alt_text="Table", contents=bubble)

#     # 使用 Line Bot API 发送 Flex Message
#     line_bot_api.reply_message(event.reply_token, flex_message)




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
