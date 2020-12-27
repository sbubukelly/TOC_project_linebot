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
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselColumn,
    ImageCarouselTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    URITemplateAction
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
            
            if isinstance(event, MessageEvent):
                if event.message.text == "開始":
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=765&q=80',
                                image_aspect_ratio='rectangle',
                                image_size="cover",
                                text='請選擇種類',
                                actions=[
                                    PostbackTemplateAction(
                                        label='粉底',
                                        text='foundation',
                                        data='A&foundation'
                                    ),
                                    PostbackTemplateAction(
                                        label='口紅',
                                        text='lipstick',
                                        data='A&lipstick'
                                    ),
                                    PostbackTemplateAction(
                                        label='腮紅',
                                        text='blush',
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
              
            if isinstance(event, PostbackEvent):       
                if event.postback.data[0:2] == "p1":  
                    line_bot_api.reply_message(  
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    thumbnail_image_url='https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=765&q=80',
                                    image_aspect_ratio= "rectangle",
                                    image_size="cover",
                                    text='請選擇種類',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='眉筆',
                                            text='eyebrow',
                                            data='A&eyebrow'
                                        ),
                                        PostbackTemplateAction(
                                            label='眼影盤',
                                            text='palette',
                                            data='A&palette'
                                        ),
                                        PostbackTemplateAction(
                                            label='蜜粉餅',
                                            text='PrPowder',
                                            data='A&PrPowder'
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
                                    thumbnail_image_url='https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=765&q=80',
                                    image_aspect_ratio="rectangle",
                                    image_size= "cover",
                                    text='請選擇種類',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='修容',
                                            text='contour',
                                            data='A&contour'
                                        ),
                                        PostbackTemplateAction(
                                            label='睫毛膏',
                                            text='mascara',
                                            data='B&mascara'
                                        ),
                                        PostbackTemplateAction(
                                            label='眼線',
                                            text='eyeliner',
                                            data='B&eyeliner'
                                        ),
                                        PostbackTemplateAction(
                                            label='遮瑕',
                                            text='concealer',
                                            data='B&concealer'
                                        )
                                    ]
                                )
                            )
                        )
 
                elif event.postback.data[0:1] == "A":
                        cosmetic = MyBest(event.postback.data[2:])  #使用者傳入的訊息文字
                        brand = []
                        name = []
                        price = []
                        img = []
                        temp = []
                        temp=cosmetic.scrape()
                        for items in temp:
                            item = items.split("|")
                            brand.append(item[0])
                            name.append(item[1])
                            price.append(item[2])
                            img.append(item[3])
                        
                        line_bot_api.reply_message(  
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='carousel template',
                                template=CarouselTemplate(
                                    columns=[
                                        CarouselColumn(
                                            thumbnail_image_url=img[9],
                                            title=  "1."+"\n" +brand[9]+"\n"+name[9],      #rank + brand + name
                                            text=price[9],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='連結2',
                                                    uri='http://example.com/2'
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[8],
                                            title=  "1."+"\n" +brand[8]+"\n"+name[8],      #rank + brand + name
                                            text=price[8],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='連結2',
                                                    uri='http://example.com/2'
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        )
               
                # elif event.postback.data[0:1] == "B":


              
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
