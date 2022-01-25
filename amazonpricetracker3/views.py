from xml.dom import NotFoundErr
import threading
import MySQLdb

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
       
        try:
            rowcount = db.updateFluctuations(db.getProducts())

            if(rowcount != -1):
                return HttpResponse('{"response_status": 201, "message": "fluctuation updated succesfully"}')
            else:
                return HttpResponse('{"response_status": 200, "message": "fluctuation already updated"}')

        except:
            return HttpResponse('{"response_status": 500, "message": "something went wrong"}')
        

