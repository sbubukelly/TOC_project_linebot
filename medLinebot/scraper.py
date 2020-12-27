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
    def scrape(self):
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
        contents = []
        name =''
        brand = ''
        rank = ''
        price = ''
        img_url = ''
        #url =[]
        temp = ''
        temp2 = ''
        first = 0
        second = 0
        for card in cards:
            
            temp = card.find("div",{"class": "c-badge-rank--default"})
            if(temp != None):
                if(temp.getText() == "PR"):
                    continue
            
            #print(rank)
            name=card.find("span",{"class": "c-panel__heading"}).getText()
            brand=card.find("span",{"class": "c-panel__sub-text"}).getText()
 
            price=card.find( "p", {"class": "c-panel__price"}).getText()

            #temp = card.find("li")
            #url.append(temp.find("a").get("href"))

            temp = card.find("img")
            if(temp != None):
                img_url=temp.get("data-original")
                print(img_url)
            elif(temp == None):
                temp = card.find("div",{"class":"carousel"})
                if(temp!=None):
                    temp= temp.get("data-images")
                    first = temp.find("https://img.") 
                    temp2 = temp[first:]
                    second = temp2.find("jpg")+3
                    img_url=temp[first:first+second]

            content =brand + "|" + name + "|" + price + "|" + img_url 
            contents.append(content)
        '''   
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
        elif(element == 'url'):
            return url
        '''
        
        return contents 

cosmetic = MyBest("foundation")
#print(cosmetic.scrape())
temp=cosmetic.scrape()
rank = []
brand = []
name = []
price = []
img = []
for items in temp:
    item = items.split("|")
    #print(item)
    brand.append(item[0])
    name.append(item[1])
    price.append(item[2])
    img.append(item[3])
print(img)
'''
print(cosmetic.scrape('brand')[9] + "\n")
print(cosmetic.scrape('name')[9] + "\n")
print(cosmetic.scrape('price')[9] + "\n")
print(cosmetic.scrape('img')[9] + "\n")
print(cosmetic.scrape('url')[9] + "\n")
'''
