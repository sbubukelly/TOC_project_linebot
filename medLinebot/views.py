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
                if event.message.text == "目錄":
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
                else:
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text="輸入「目錄」來選取想知道的品項排行歐!(moon grin)(moon grin)"))
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
                                            data='x&mascara'
                                        ),
                                        PostbackTemplateAction(
                                            label='眼線',
                                            text='eyeliner',
                                            data='y&eyeliner'
                                        ),
                                        PostbackTemplateAction(
                                            label='遮瑕',
                                            text='concealer',
                                            data='z&concealer'
                                        )
                                    ]
                                )
                            )
                        )
 
                elif event.postback.data[0:1] == "x":
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
                                            label='纖長型睫毛膏',
                                            text='纖長型睫毛膏',
                                            data='m1&mascara'
                                        ),
                                        PostbackTemplateAction(
                                            label='濃密型睫毛膏',
                                            text='濃密型遮瑕膏',
                                            data='m2&mascara'
                                        )

                                    ]
                                )
                            )
                        )    
        
                elif event.postback.data[0:1] == "y":
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
                                            label='眼線液',
                                            text='眼線液',
                                            data='m1&eyeliner'
                                        ),
                                        PostbackTemplateAction(
                                            label='眼線鉛筆',
                                            text='眼線鉛筆',
                                            data='m2&eyeliner'
                                        )

                                    ]
                                )
                            )
                        )    
        
                elif event.postback.data[0:1] == "z":
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
                                            label='黑眼圈遮瑕膏',
                                            text='黑眼圈遮瑕膏',
                                            data='m1&concealer'
                                        ),
                                        PostbackTemplateAction(
                                            label='黑斑遮瑕膏',
                                            text='黑斑遮瑕膏',
                                            data='m2&concealer'
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
                        url = []
                        temp = []
                        temp=cosmetic.scrape()
                        for items in temp:
                            item = items.split("|")
                            brand.append(item[0])
                            name.append(item[1])
                            price.append(item[2])
                            img.append(item[3])
                            url.append(item[4])
                        
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
                                                    label='購買連結',
                                                    uri=url[9]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[8],
                                            title=  "2."+"\n" +brand[8]+"\n"+name[8],      #rank + brand + name
                                            text=price[8],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[8]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[7],
                                            title=  "3."+"\n" +brand[7]+"\n"+name[7],      #rank + brand + name
                                            text=price[7],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[7]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[6],
                                            title=  "4."+"\n" +brand[6]+"\n"+name[6],      #rank + brand + name
                                            text=price[6],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[6]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[5],
                                            title=  "5."+"\n" +brand[5]+"\n"+name[5],      #rank + brand + name
                                            text=price[5],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[5]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[4],
                                            title=  "6."+"\n" +brand[4]+"\n"+name[4],      #rank + brand + name
                                            text=price[4],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[4]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[3],
                                            title=  "7."+"\n" +brand[3]+"\n"+name[3],      #rank + brand + name
                                            text=price[3],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[3]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[2],
                                            title=  "8."+"\n" +brand[2]+"\n"+name[2],      #rank + brand + name
                                            text=price[2],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[2]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[1],
                                            title=  "9."+"\n" +brand[1]+"\n"+name[1],      #rank + brand + name
                                            text=price[1],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[1]
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            thumbnail_image_url=img[0],
                                            title=  "10."+"\n" +brand[0]+"\n"+name[0],      #rank + brand + name
                                            text=price[0],        #price 
                                            actions=[
                                                URITemplateAction(
                                                    label='購買連結',
                                                    uri=url[0]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        )
               
                elif event.postback.data[0:2] == "m1":
                    cosmetic = MyBest(event.postback.data[3:])  #使用者傳入的訊息文字
                    brand = []
                    name = []
                    price = []
                    img = []
                    url = []
                    temp = []
                    temp=cosmetic.scrape()
                    for items in temp:
                        item = items.split("|")
                        brand.append(item[0])
                        name.append(item[1])
                        price.append(item[2])
                        img.append(item[3])
                        url.append(item[4])
                        
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
                                                label='購買連結',
                                                uri=url[9]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[8],
                                        title=  "2."+"\n" +brand[8]+"\n"+name[8],      #rank + brand + name
                                        text=price[8],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[8]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[7],
                                        title=  "3."+"\n" +brand[7]+"\n"+name[7],      #rank + brand + name
                                        text=price[7],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[7]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[6],
                                        title=  "4."+"\n" +brand[6]+"\n"+name[6],      #rank + brand + name
                                        text=price[6],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[6]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[5],
                                        title=  "5."+"\n" +brand[5]+"\n"+name[5],      #rank + brand + name
                                        text=price[5],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[5]
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    )

                elif event.postback.data[0:2] == "m2":
                    cosmetic = MyBest(event.postback.data[3:])  #使用者傳入的訊息文字
                    brand = []
                    name = []
                    price = []
                    img = []
                    url = []
                    temp = []
                    temp=cosmetic.scrape()
                    for items in temp:
                        item = items.split("|")
                        brand.append(item[0])
                        name.append(item[1])
                        price.append(item[2])
                        img.append(item[3])
                        url.append(item[4])
                        
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='carousel template',
                            template=CarouselTemplate(
                                  columns=[
                                    CarouselColumn(
                                    thumbnail_image_url=img[4],
                                        title=  "1."+"\n" +brand[4]+"\n"+name[4],      #rank + brand + name
                                        text=price[4],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[4]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[3],
                                        title=  "2."+"\n" +brand[3]+"\n"+name[3],      #rank + brand + name
                                        text=price[3],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[3]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[2],
                                        title=  "3."+"\n" +brand[2]+"\n"+name[2],      #rank + brand + name
                                        text=price[2],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[2]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[1],
                                        title=  "4."+"\n" +brand[1]+"\n"+name[1],      #rank + brand + name
                                        text=price[1],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[1]
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=img[0],
                                        title=  "5."+"\n" +brand[0]+"\n"+name[0],      #rank + brand + name
                                        text=price[0],        #price 
                                        actions=[
                                            URITemplateAction(
                                                label='購買連結',
                                                uri=url[0]
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    )

                
                    
              
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
