from xml.dom import NotFoundErr
from mysql.connector.errors import DatabaseError


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .product.Product import Product
from .utils import utils, db

import json



def home(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")

def getPrice(request):
    time = utils.getTime()
    print(f"time of request is {time['date']} {time['time']}")
    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
        product = Product(body['url'])
        return HttpResponse( product.toString() )

    except ValueError as v:
        return HttpResponse(f'{{"error": 1, "errorMessage": "{v}"}}')
    
    except NotFoundErr:
        # if name not found error occurs try again
        print("recurring views.getPrice")
        return getPrice(request)
        # return HttpResponse(r'{"error": 1, "errorMessage": "NotFoundErr in views.getPrice"}')

@csrf_exempt
def fluctuations(request):
    if request.method == "GET":
        for f in db.getFluctuations():
            print(f)
    
        return HttpResponse('{"response_status":"200" ,"message":"todays Fluctuations are logged to console"}')

    elif request.method == "POST":
        time = utils.getTime()
        result = db.getFluctuationsNotRecordedOn(time["date"])

        if result == -1:
            return HttpResponse('{"error": 1 ,"message" : "todays fluctuations are already recorded"}')

        unRecordedFluctuations = []

        for r in result:
            unRecordedFluctuations.append(utils.getTodaysPrice(r[2]))

        db.updateFluctuations(unRecordedFluctuations)
        
        print("todays Fluctuations recorded")
    
        return HttpResponse('{"response_status":"200" ,"message":"todays Fluctuations recorded"}')


@csrf_exempt
def product(request):
    if (request.method == "POST"):
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
            product1 = Product(body['url'])

            if(db.isProductExists(product1)):
                return HttpResponse('{"response_status": 200, "message": "product alredy exists"}')
            
            rowcount = db.registerProduct(product1)
            if(rowcount != -1):
                return HttpResponse('{"response_status": 201, "message": "product registerd succesfully"}')
            else:
                return HttpResponse(r'{"error": 1, "errorMessage": "product registration failed"}')

        except NotFoundErr:
            print("reccuring views.product")
            # if name not found error occurs try again
            return product(request)
        except ValueError as v:
            print(v)
            return HttpResponse(f'{{"error": 1, "errorMessage": "{v}"}}')

@csrf_exempt
def users(request):
   if request.method == "POST":
        response = {
            "message": "working on this api"
        }
    
        try:
            body_unicode = request.body.decode("utf-8")
            creds = json.loads(body_unicode)
            
            if(db.isUserExists(creds["username"]) != True):
                db.registerUser(creds)
                response["response_status"] = 200
                response["message"] = "user succesfully registered"
            else:
                response["response_status"] = 201
                response["message"] = "user already exists"

            return HttpResponse(json.dumps(response))
        except DatabaseError as de:
            print(de)
            response["error"] = 1
            response["message"] = "Database error occured"
            return HttpResponse(json.dumps(response))
        except KeyError as k:
            print(k)
            response["error"] = 400
            response["message"] = f'key missing : {k}'
            return HttpResponse(json.dumps(response))



        
