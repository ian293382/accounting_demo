

def create_single_text_message(message):
    
    if message == 'ありがとう':
        message = 'どういたしまして！'
    # test_message = [
    #             {
    #                 'type': 'text',
    #                 'text': message,
    #             }
    #         ]
    
    
    test_message = [
        {
            "type":"text",
            "text":"Hello, user"
        },
        {
            "type":"text",
            "text":"May I help you?"
        }
    ]
    return test_message



# def create_flex_message():
#     flex_message =  [
#     {
#       "type": "flex",
#       "altText": "This is a Flex Message",
#       "contents": {
#         "type": "bubble",
#         "body": {
#           "type": "box",
#           "layout": "horizontal",
#           "contents": [
#             {
#               "type": "text",
#               "text": "Hello,"
#             },
#             {
#               "type": "text",
#               "text": "World!"
#             }
#           ]
#         }
#       }
#     }
#   ]
#     return [flex_message]