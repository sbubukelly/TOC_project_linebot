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
                    
            elif event.postback.data[0:2] == "p1":  
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
                    '''
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=cosmetic.scrape())
                    )
                    '''
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='carousel template',
                            template=CarouselTemplate(
                                columns=[
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[9],
                                        title= cosmetic.scrape('rank')[9] +"."+"\n" +cosmetic.scrape('name')[9],      #rank + brand + name
                                        text=cosmetic.scrape('price')[9],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[8],
                                        title= cosmetic.scrape('rank')[8] +"."+"\n" +cosmetic.scrape('name')[8],      #rank + brand + name
                                        text=cosmetic.scrape('price')[8],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[7],
                                        title= cosmetic.scrape('rank')[7] +"."+"\n" +cosmetic.scrape('name')[7],      #rank + brand + name
                                        text=cosmetic.scrape('price')[7],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[6],
                                        title= cosmetic.scrape('rank')[6] +"."+"\n" +cosmetic.scrape('name')[6],      #rank + brand + name
                                        text=cosmetic.scrape('price')[6],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[5],
                                        title= cosmetic.scrape('rank')[5] +"."+"\n" +cosmetic.scrape('name')[5],      #rank + brand + name
                                        text=cosmetic.scrape('price')[5],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[4],
                                        title= cosmetic.scrape('rank')[4] +"."+"\n" +cosmetic.scrape('name')[4],      #rank + brand + name
                                        text=cosmetic.scrape('price')[4],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[3],
                                        title= cosmetic.scrape('rank')[3] +"."+"\n" +cosmetic.scrape('name')[93],      #rank + brand + name
                                        text=cosmetic.scrape('price')[3],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[2],
                                        title= cosmetic.scrape('rank')[2] +"."+"\n" +cosmetic.scrape('name')[2],      #rank + brand + name
                                        text=cosmetic.scrape('price')[2],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[1],
                                        title= cosmetic.scrape('rank')[1] +"."+"\n" +cosmetic.scrape('name')[1],      #rank + brand + name
                                        text=cosmetic.scrape('price')[1],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=cosmetic.scrape('img')[0],
                                        title= cosmetic.scrape('rank')[0] +"."+"\n" +cosmetic.scrape('name')[0],      #rank + brand + name
                                        text=cosmetic.scrape('price')[0],        #price 
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
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
