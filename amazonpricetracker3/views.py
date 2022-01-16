from django.http import HttpResponse
from .product.Product import Product
import json

def home(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")

def getPrice(request):
    body_unicode = request.body.decode('utf-8')
    print(body_unicode)
    body = json.loads(body_unicode)
    product = Product(body['url'])
    return HttpResponse( product.toString() )