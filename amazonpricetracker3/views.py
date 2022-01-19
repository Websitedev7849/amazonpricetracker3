from xml.dom import NotFoundErr
from django.http import HttpResponse
from .product.Product import Product
import json
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

print(f"today's date on server is {today}")

def home(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")

def getPrice(request):
    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
        product = Product(body['url'])
        return HttpResponse( product.toString() )

    except ValueError:
        return HttpResponse(r'{"error": 1, "errorMessage": "JsonDecode Error in views.getPrice"}')
    
    except NotFoundErr:
        return HttpResponse(r'{"error": 1, "errorMessage": "NotFoundErr in views.getPrice"}')