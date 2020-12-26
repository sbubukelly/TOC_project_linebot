from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)
from .scraper import MyBest

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                
                if event.message.text == "開始":

                    line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                text='請選擇種類',
                                actions=[
                                    PostbackTemplateAction(
                                        label='foundation',
                                        text='粉底',
                                        data='A&foundation'
                                    ),
                                    PostbackTemplateAction(
                                        label='口紅',
                                        text='口紅',
                                        data='A&lipstick'
                                    ),
                                    PostbackTemplateAction(
                                        label='腮紅',
                                        text='腮紅',
                                        data='A&blush'
                                    ),
                                    PostbackTemplateAction(
                                        label='更多',
                                        text='更多',
                                        data='p1&more'
                                    )

                                ]
                            )
                        )
                    )
            
            elif event.postback.data[0:2] == "p1":  
                line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                text='請選擇種類',
                                actions=[
                                    PostbackTemplateAction(
                                        label='眉筆',
                                        text='眉筆',
                                        data='A&eyebrow'
                                    ),
                                    PostbackTemplateAction(
                                        label='眼影盤',
                                        text='眼影盤',
                                        data='A&palette'
                                    ),
                                    PostbackTemplateAction(
                                        label='蜜粉餅',
                                        text='蜜粉餅',
                                        data='A&PrPoweder'
                                    ),
                                    PostbackTemplateAction(
                                        label='更多',
                                        text='更多',
                                        data='p2&more'
                                    )

                                ]
                            )
                        )
                    )    
                        
            elif event.postback.data[0:2] == "p2":
                line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                text='請選擇種類',
                                actions=[
                                    PostbackTemplateAction(
                                        label='修容',
                                        text='修容',
                                        data='A&contour'
                                    ),
                                    PostbackTemplateAction(
                                        label='睫毛膏',
                                        text='睫毛膏',
                                        data='A&mascara'
                                    ),
                                    PostbackTemplateAction(
                                        label='眼線',
                                        text='眼線',
                                        data='A&eyeliner'
                                    ),
                                    PostbackTemplateAction(
                                        label='遮瑕',
                                        text='遮瑕',
                                        data='A&concealer'
                                    )
                                ]
                            )
                        )
                    )
                
            else:
                    cosmetic = MyBest(event.message.text)  #使用者傳入的訊息文字
 
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=cosmetic.scrape())
                    )
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
