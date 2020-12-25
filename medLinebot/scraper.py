from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
 
 
# 美食抽象類別
class Cosmetic(ABC):
 
    def __init__(self, type):
        self.type =type #化妝品種類
 
    def convert(type):
        if(self.type == "foundation"):
            return '131'
        elif(self.type == "lipstick"):
            return '1193'
        elif(self.type == "blush"):
            return '114956'    
        elif(self.type == "eyebrow"):
            return '114944'
        elif(self.type == "palette"):
            return '12653'
        elif(self.type == "PrPowder"):   # Pressed  Powder
            return '68880'
        elif(self.type == "contour"):
            return '6151'
        elif(self.type == "mascara"):
            return '4730'
        elif(self.type == "eyeliner"):
            return '1684'
        elif(self.type == "mascara"):
            return '4730'
        elif(self.type == "concealer"):
            return '472'

    @abstractmethod
    def scrape(self):
        pass
 
 
# My best爬蟲
class MyBest(Cosmetic):
 
    def scrape(self):
        response = requests.get("https://my-best.tw/" + convert(self.type) )
 
        soup = BeautifulSoup(response.content, "html.parser")
        
        cards = soup.find_all('div', {'class': 'p-press__part js-parts','data-type':'item_part'})
        content = ""
        for card in cards:
            name = card.find("h3").getText()
 
            price = card.find( "p", {"class": "c-panel__price"}).getText()
 
            # expalin = card.find(  ).getText()
            info = card.select('tr')
            content = f"{name} \n{price}\n\n"
            if(len(info) < 0):
              pass
            else:
                for x in info: 
                    content += f"{x.getText()}\n"
   
            content += "\n"
            #content = f"{name} \n\n"
            print(content)
            return content
        