import json
import os

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (ApiClient, AudioMessage, Configuration,
                                  ImageMessage, MessagingApi, MessagingApiBlob,
                                  ReplyMessageRequest,
                                  ShowLoadingAnimationRequest, TextMessage)
from linebot.v3.webhooks import (AudioMessageContent, ImageMessageContent,
                                 MessageEvent, StickerMessageContent,
                                 TextMessageContent)


configuration = Configuration(
    access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.show_loading_animation(
            ShowLoadingAnimationRequest(
                chat_id=event.source.user_id,
                # loading_seconds=5
            )
        )
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

def lambda_handler(event, context):
    try: 
        body = event['body']
        signature = event['headers']['x-line-signature']
        handler.handle(body, signature)
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
