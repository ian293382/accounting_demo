from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Line_User
from accounts.models import User
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, 
    TemplateSendMessage, 
    PostbackAction,
    ButtonsTemplate,
    PostbackEvent,
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent
from django.http import HttpResponse, HttpResponseBadRequest

# Line Bot API初始化
line_bot_api = LineBotApi('+30MYidMCTmW/v6LBswcci5ftP4wYnmOV+jJ0bqpj2RSwIqnVPv7poIAG2AsZB/5C8UkIcLPMmLXzfOLYo7++cGJvEL3sQo5HbwP7kHBnSH2zz8dmunTom+aKNK65uJwfOeku3c5m7ZLLqOp06PBVwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('04e9d3cec27b730cbcede1ee9c4c8c9b')

from financial_records.models import Category,FinancialRecord
from groups.models import Groups 


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
        if events and 'source' in events[0] and 'userId' in events[0]['source']:
            user_id = events[0]['source']['userId']
        else:
           
            user_id = None  
        # print('user_id:', user_id)
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse('OK', status=200)
    else:
        return HttpResponseBadRequest()

# 邏輯訊息
# 1.是否找到 Line_user 2.命令邏輯 3.綁定邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_input_email = event.message.text
    try:
        line_user = Line_User.objects.get(line_user_id=user_id)
        
        # 如果找到，表示用戶已經綁定
        command = event.message.text
        if command.startswith('/b') or command.startswith('/c'):
            parts = command.split()
            record_type = '支出' if command.startswith('/b') else '收入'

            if len(parts) < 3:
                response_message = f"指令格式不正確。使用：{command} [描述] [幣值]"
            else:
                amount = parts[1]
                record_name = parts[2]
                description = " ".join(parts[3:]) if len(parts) > 3 else None
                currency = 1.0

                # Pass user_id to create_record
                record = create_record(user_id, record_type, amount, record_name, description, currency)

                response_message = f"已創建{record_type}紀錄：{record_name}，{record_type}金額：{amount}，描述{record.description}，剩下餘額：{record.balance}"
        else:
            response_message = "無效指令。請使用：/b 100 一支筆 [描述] 或 /c 50000 收入 [描述] [幣值]，還是你想跟我真人對話>///<"

    except Line_User.DoesNotExist:
        # 如果找不到，表示用戶未綁定
        try:
            # 用 email 找尋 User
            user = User.objects.get(email=user_input_email)
            # 如果 line_user_id 是 null，賦予新的值並保存修改
            if not user.line_user_id:
                user.line_user_id = user_id
                user.save()
                line_user = Line_User.objects.create(user=user, line_user_id=user_id)
                line_user.save()
                response_message = f"已成功綁定！用戶 {user.username} 與 Email {user_input_email} 已經成功關聯。"
            else:
                # 如果 line_user_id 已存在，返回錯誤訊息
                response_message = f"錯誤：此 Email 已經綁定過用戶 {user.username}，將反傳表單請您再次選取。"
                send_bind_user_buttons(user_id)
            
        except User.DoesNotExist:
            # 如果找不到用戶，返回錯誤訊息並同時發送按鈕選單
            response_message = f"歡迎你使用本會計系統，稍後會傳遞選單供使用者選取請稍待耐心。"
            send_bind_user_buttons(user_id)

    # 回覆用戶
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))

def send_bind_user_buttons(user_id):
    welcome_message = "歡迎加入！請問是否要進行用戶綁定功能："
    buttons_template = ButtonsTemplate(
        text=welcome_message,
        actions=[
            PostbackAction(
                label='綁定帳戶',
                data='action=bind_form'
            ),
            PostbackAction(
                label='創建帳戶',
                data='action=create_account'
            ),
        ]
    )

    template_message = TemplateSendMessage(
        alt_text='綁定表單',
        template=buttons_template
    )

    # 在這裡發送按鈕消息
    line_bot_api.push_message(user_id, template_message)


# 在 FollowEvent 中添加按鈕模板
@handler.add(FollowEvent)
def handle_follow_event(event):
    user_id = event.source.user_id
    print('user_id:', user_id)
    print(f'User {user_id} followed the bot.')

    send_bind_user_buttons(user_id)

# 新增方法處理用戶綁定事件
@handler.add(PostbackEvent)
def handle_postback_event(event):
    user_id = event.source.user_id
    postback_data = event.postback.data

    if postback_data == 'action=bind_form':
        # 在用戶點擊 "綁定帳戶" 後回傳提示請輸入 Email 的消息
        response_message = "請輸入你的 Email，將使用 Email 與網路用戶進行綁定。"
        line_bot_api.push_message(user_id, TextSendMessage(text=response_message))

    if postback_data == 'action=create_account':
        try:
            line_user = Line_User.objects.get(line_user_id=user_id)

            # 如果找到，則回傳錯誤訊息 這樣就不用跳到報錯了也不用處理例外訊息
            error_message = "用戶已經存在請使用/b 100 一支筆 [描述] 或 /c 50000 收入 [描述] [幣值] 進行紀錄唷。"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))

        except Line_User.DoesNotExist:
            
                # 如果找不到相應的條目，創建一個新的 User 實例
                new_user_instance = User(username=f"line_user_{user_id}", password="dummy_password", line_user_id=user_id)
                new_user_instance.save()

                # 使用新創建的 User 實例創建 LineUser 實例
                new_line_user = Line_User(user=new_user_instance, line_user_id=user_id)
                new_line_user.save()

                print(f"Created a new line_user with user_id: {user_id}")    
                welcome_message = "歡迎加入！請使用：/b 100 一支筆 [描述] 或 /c 50000 收入 [描述] [幣值] 進行記錄吧"
                
                line_bot_api.push_message(user_id, TextSendMessage(text=welcome_message))

def create_record(user_id, record_type, amount, record_name, description=None, currency=1):
    # Find the User using user_id
    user = get_object_or_404(User, line_user_id= user_id)

    # Create group, category, financial_record
    group, created = Groups.objects.get_or_create(group_name=f"損益表（line自動創建)", created_by=user)
    category, created = Category.objects.get_or_create(group=group, name=f"{record_type}(由line自動創建)", created_by=user)
    record = FinancialRecord.objects.create(
        group=group,
        name=record_name,
        description=description,
        created_by=user
    )

    # 根據記錄類型設置
    if record_type == '支出':
        record.debit = amount
    elif record_type == '收入':
        record.credit = amount

    if record.description == None:
        record.description = '為空白'
    else :
        record.description = description


    record.currency = currency
    record.save()

    record.category.add(category)
    # 要顯示的只有record的部分 group category不用加入
    return record


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    user_id = event.source.user_id
    print(event)
    print(f'User {user_id} unfollowed the bot.')