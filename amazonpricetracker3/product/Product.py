import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()


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
        self.url = url[:url.find('ref', 0)]

        self.page = requests.get( self.url, headers=headers)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

        # self.raw_data = self.getRawData()
        self.asin = self.get_asin()
        self.name = self.getName()
        self.price = self.getPrice()


    """
    def getRawData(self):
        url = "https://api.rainforestapi.com/request?api_key=" + os.getenv("RAINFOREST_API_KEY") +"&type=product&url=" + self.url
        # print(requests.get(url).text)
        return json.loads(requests.get(url).text)
    """

    def getName(self):
        # self.url = https://www.amazon.in/Redmi-9A-Midnight-2GB-32GB/dp/B08697N43G/ref=lp_1389401031_1_5?th=1
        u = urlparse(self.url)

        # u.path.split('/)[1:] = ['Redmi-9A-Midnight-2GB-32GB', 'dp', 'B08697N43G', 'ref=lp_1389401031_1_5']
        u = u.path.split('/')[1:]
        
        name = u[0]
        name = name.replace('-', ' ')
        return name
    
    def get_asin(self):
        # self.url = https://www.amazon.in/Redmi-9A-Midnight-2GB-32GB/dp/B08697N43G/ref=lp_1389401031_1_5?th=1
        u = urlparse(self.url)

        # u.path.split('/)[1:] = ['Redmi-9A-Midnight-2GB-32GB', 'dp', 'B08697N43G', 'ref=lp_1389401031_1_5']
        u = u.path.split('/')[1:]

        # return 3 element which is asin
        return u[2]

    def getPrice(self):

        price = self.soup.find("span", {"class": "a-offscreen"})

        priceToReturn = price.text[1:].replace(",", "")

        return float(priceToReturn)

    def toString(self):
        return  "{" + f' "asin": "{self.asin}", "name": "{self.name}", "price" : {self.price}, "url" : "{self.url}" ' + "}"

