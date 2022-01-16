from xml.dom import NotFoundErr
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
        
        self.asin = self.get_asin()
        self.link = self.getLink()

        self.page = requests.get( self.link, headers=headers)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        
        self.name = self.getName()
        self.price = self.getPrice()

    
    def getLink(self):
        return "https://www.amazon.in/dp/" + self.asin

    # using soup
    def getName(self):
        nameTag = self.soup.find(id="productTitle")
        if nameTag == None:
            raise NotFoundErr("Name Not Found in Product.py/getName")
        return nameTag.text.strip()
    
    def get_asin(self):
        u = urlparse(self.url)

        # u.path.split('/)[1:] = ['Redmi-9A-Midnight-2GB-32GB', 'dp', 'B08697N43G', 'ref=lp_1389401031_1_5']
        u = u.path.split('/')[1:]

        return u[u.index("dp") + 1]

    # using soup
    def getPrice(self):

        price = self.soup.find("span", {"class": "a-offscreen"})

        if price == None:
            raise NotFoundErr("Price Not Found in Product.py/getPrice")

        priceToReturn = price.text[1:].replace(",", "") if price != None else -1

        return float(priceToReturn)

    def toString(self):
        # return self.rawData
        return  "{" + f' "asin": "{self.asin}", "name": "{self.name}", "price" : {self.price}, "link" : "{self.link}" ' + "}"

