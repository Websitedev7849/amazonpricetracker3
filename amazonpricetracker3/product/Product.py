from dotenv import load_dotenv
load_dotenv()

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json



"""
{ 
    "asin": "B08L5VPTDK",
    "name": "New Apple iPhone 12 Pro (256GB) - Gold",
    "price": "99,900.00"
    "url": "https://www.amazon.in/New-Apple-iPhone-Pro-256GB/dp/B08L5VPTDK?ref_=Oct_DLandingS_D_9085df6d_60&smid=A14CZOWI0VEHLG"
    "date": "YYYY-MM-DD"
}
"""

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}


class Product:



    def __init__(self, url):
        self.url = url
        
        self.page = requests.get( url, headers=headers)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

        self.rawData = self.getRawData()

        self.link = self.getLink()
        self.asin = self.get_asin()
        self.name = self.getName()
        self.price = self.getPrice()


    
    def getRawData(self):
        url = "https://api.rainforestapi.com/request?api_key=" + os.getenv("RAINFOREST_API_KEY") +"&type=product&url=" + self.url
        # print(requests.get(url).text)
        return json.loads(requests.get(url).text)
    
    def getLink(self):
        return self.rawData["product"]["link"]

    def getName(self):
        return self.rawData["product"]["title"]
    
    def get_asin(self):
        return self.rawData["product"]["asin"]

    def getPrice(self):

        price = self.soup.find("span", {"class": "a-offscreen"})

        # priceToReturn = price.text[1:].replace(",", "")
        priceToReturn = price.text[1:].replace(",", "") if price != None else "PRICE IS NONE"

        return priceToReturn

    def toString(self):
        # return self.rawData
        return  "{" + f' "asin": "{self.asin}", "name": "{self.name}", "price" : {self.price}, "link" : "{self.link}" ' + "}"

