from xml.dom import NotFoundErr
import threading

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .product.Product import Product
from .utils.utils import getTime
from .utils import db

import json



def home(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")

def getPrice(request):
    time = getTime()
    print(f"time of request is {time['date']} {time['time']}")
    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
        product = Product(body['url'])
        return HttpResponse( product.toString() )

    except ValueError:
        return HttpResponse(r'{"error": 1, "errorMessage": "JsonDecode Error in views.getPrice"}')
    
    except NotFoundErr:
        return HttpResponse(r'{"error": 1, "errorMessage": "NotFoundErr in views.getPrice"}')

@csrf_exempt
def fluctuations(request):
    if request.method == "GET":
        for f in db.getFluctuations():
            print(f)
        return HttpResponse("flucutaions are logged to console")

    elif request.method == "POST":
        for product in db.getProducts():
            threading.Thread(target=db.getTodaysPrice, args=( product[0], )).start()

        return HttpResponse("todays flucutaions are logged to console")
        

