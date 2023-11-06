from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from utils import message_creater
from line_bot.line_message import LineMessage


# @csrf_exempt
# def index(request):
#     if request.method == 'POST':
#         request = json.loads(request.body.decode('utf-8'))
#         data = request['events'][0]
#         message = data['message']
#         reply_token = data['replyToken']
#         line_message = LineMessage(message_creater.create_single_text_message(message['text']))
#         line_message.reply(reply_token)
#         return HttpResponse("ok")
    

@csrf_exempt
def index(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        data = request_data['events'][0]
        message = data['message']
        reply_token = data['replyToken']

        if message['text'].startswith('/bind_email '):
            # 收到使用者發的地址
            email = message['text'].replace('/bind_email ', '')
            
            # 在這裡完成會員登錄
            reply_message = message_creater.create_single_text_message(f'已成功绑定邮箱地址：{email}')
        else:
            # 处理其他消息
            reply_message = message_creater.create_single_text_message('无法识别的命令，请输入 /bind_email 邮箱地址。')

        # 发送回复消息
        line_message = LineMessage(reply_message)
        line_message.reply(reply_token)

        return HttpResponse("ok")