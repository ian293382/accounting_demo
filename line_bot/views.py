from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from utils import message_creater
from line_bot.line_message import LineMessage


@csrf_exempt
def index(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print('request:', json_data)
        data = json_data['events'][0]
        message = data['message']
        reply_token = data['replyToken']
        line_message = LineMessage(message_creater.create_single_text_message(message))
        line_message.reply(reply_token)

        return HttpResponse("ok")

