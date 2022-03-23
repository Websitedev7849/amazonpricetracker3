from datetime import datetime
from ..product.Product import Product

from xml.dom import NotFoundErr


def getTime():
    time24hourformat = datetime.today().strftime('%H:%M')
    d = datetime.strptime(time24hourformat, '%H:%M')
    today = {
        "date" : datetime.today().strftime('%Y-%m-%d'),
        "time": d.strftime("%I:%M %p")
    }
    return today

def getTodaysPrice(link):
    try:
        product = Product(link)
        return product.toString()

    except NotFoundErr:
        # if name not found error occurs try again
        print("recurring utils.getTodaysprice for link :" + link)
        return getTodaysPrice(link)
    
