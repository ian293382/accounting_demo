from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json



REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
PUSH_ENDPOINT_URL = "https://api.line.me/v2/bot/message/push"
ACCESSTOKEN = 'kOeXM+8gIjtaPPKhrVPd+sqDCsjwtcN+1dJbFQBqbEX3A2i0hVW9oDaMYb55gM1f+5wnlal1Xmp61BZTiJON6CrJsa4A5hwAuXJDe/Sr8nN8/2DHZLY3jCU3AvxwrkMnwW8vIUwDIYKhPvfnbC7kdgdB04t89/1O/w1cDnyilFU='

# 使用Bearer令牌進行身份驗證
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': self.messages
        }
        print(body)

        print('HEADER:',HEADER)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)

    def push(self, to):
        body = {
            'to': 'Ub0b89abee8a59ea076f86c88c7eaf6fc',
            'messages': self.messages
        }
        print('Push Body:', body)
