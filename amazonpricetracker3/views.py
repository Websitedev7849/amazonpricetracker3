from xml.dom import NotFoundErr
from django.http import HttpResponse

from .product.Product import Product
from .utils.utils import getTime

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

