from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
 
 
# 美食抽象類別
class Cosmetic(ABC):
 
    def __init__(self, type):
        self.type =type #化妝品種類

    @abstractmethod
    def scrape(self):
        pass
 
 
# My best爬蟲
class MyBest(Cosmetic):
    def scrape(self, element):
        convert = ''
        if(self.type == "foundation"):
            convert = '131'
        elif(self.type == "lipstick"):
            convert = '1193'
        elif(self.type == "blush"):
            convert = '114956'    
        elif(self.type == "eyebrow"):
            convert = '114944'
        elif(self.type == "palette"):
            convert = '12653'
        elif(self.type == "PrPowder"):   # Pressed  Powder
            convert = '68880'
        elif(self.type == "contour"):
            convert = '6151'
        elif(self.type == "mascara"):
            convert = '4730'
        elif(self.type == "eyeliner"):
            convert = '1684'
        elif(self.type == "concealer"):
            convert = '472'

        response = requests.get("https://my-best.tw/" + convert )
 
        soup = BeautifulSoup(response.content, "html.parser")
        
        cards = soup.find_all('div', {'class': 'p-press__part js-parts','data-type':'item_part'})
        content = ""
        name =[]
        brand = []
        rank = []
        price = []
        img_url = []
        temp = ''
        for card in cards:
            temp = card.find("div",{"class": "c-badge-rank--default"})
            if(temp == None):
                temp = card.find("div",{"class": "c-badge-rank--bronze"})
                if(temp == None):
                    temp = card.find("div",{"class": "c-badge-rank--silver"})
                    if(temp == None):
                        temp = card.find("div",{"class": "c-badge-rank--gold"})
            elif(temp.getText() == "PR"):
                continue
            rank.append(temp.getText())
            #print(rank)
            name.append(card.find("span",{"class": "c-panel__heading"}).getText())
            brand.append(card.find("span",{"class": "c-panel__sub-text"}).getText())
 
            price.append(card.find( "p", {"class": "c-panel__price"}).getText())
 
            img_url.append(card.find("img").get("data-original"))
            # expalin = card.find(  ).getText()
            info = card.select('tr')
            #content += f"{name} \n{price}\n\n"
            #content += f"{rank.getText()}\n{name} \n{price}\n\n"
            if(len(info) < 0):
              pass
            else:
                for x in info: 
                    content += f"{x.getText()}\n"
   
            content += "\n"
            #content = f"{name} \n\n"
            #print(content)
        if(element == 'brand'):
            return brand
        elif(element == 'name'):
            return name
        elif(element == 'price'):
            return price
        elif(element == 'rank'):
            return rank
        elif(element == 'img'):
            return img_url
        else:
            return content
 
cosmetic = MyBest("lipstick")
print(cosmetic.scrape('brand')[5] + "\n")
print(cosmetic.scrape('name')[5] + "\n")
print(cosmetic.scrape('price')[5] + "\n")
print(cosmetic.scrape('img')[5] + "\n")
