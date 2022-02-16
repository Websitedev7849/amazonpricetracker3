import threading
from xml.dom import NotFoundErr
from mysql.connector.errors import DatabaseError


from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .product.Product import Product
from .utils import utils, db

import json



def home(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")

def getPrice(request):
    if(request.method == "GET"):
        
        response = {}

        time = utils.getTime()
        print(f"time of request is {time['date']} {time['time']}")
        body_unicode = request.body.decode('utf-8')
        try:

            product = None

            try:
                body = json.loads(body_unicode)
                product = Product(body['url'])

            except ValueError:
                queryDictUnParsed = request.META["QUERY_STRING"]
                queryDict = QueryDict(queryDictUnParsed);
                product = Product(queryDict["url"])
        
            return HttpResponse( product.toString() , status = 200)

        except NotFoundErr:
            # if name not found error occurs try again
            print("recurring views.getPrice")
            return getPrice(request)
            
        except KeyError as k:
            print("KeyError in GET /views.getprice")
            print(k)
            response["message"] = f'Json key missing : {k}'
            return JsonResponse(response, status=400)

        except Exception as e:
            print("Exeption in GET /views.getprice")
            print(e)
            response["message"] = f"{e}"
            return JsonResponse(response, status = 500)
    else:
        response = {}
        response["message"] = "Only GET request supported"
        return JsonResponse(response, status = 400)

@csrf_exempt
def fluctuations(request):
    if request.method == "GET":
        response = {}

        for f in db.getFluctuations():
            print(f)
        response["message"] = "todays Fluctuations are logged to console"
        return JsonResponse(response, status = 200)

    elif request.method == "POST":
        response = {}
        try:
            time = utils.getTime()
            result = db.getFluctuationsNotRecordedOn(time["date"])

            if result == -1:
                response["message"] = "todays fluctuations are already recorded"
                return JsonResponse(response, status = 201)
                

            unRecordedFluctuations = []
            myThreads = []

            # for r in result:
                # unRecordedFluctuations.append(utils.getTodaysPrice(r[2]))

            for r in result:
                t = threading.Thread(target=unRecordedFluctuations.append, args=( utils.getTodaysPrice(r[2]), ) )
                t.start()
                myThreads.append(t)
            
            for t in myThreads:
                t.join()

            db.updateFluctuations(unRecordedFluctuations)
            
            print("todays Fluctuations recorded")
        
            response["message"] = "todays Fluctuations recorded"
            return JsonResponse(response, status = 200)
        except Exception as e:
            print(e)
            response["message"] = f"{e}"
            return JsonResponse(response, status = 500)

@csrf_exempt
def product(request):
    if (request.method == "POST"):
        response = {}
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
            product1 = Product(body['url'])

            if(db.isProductExists(product1)):
                response["message"] = "product already exists"
                return JsonResponse(response, status = 201)
            
            rowcount = db.registerProduct(product1)
            if(rowcount != -1):
                response["message"] = "product registerd succesfully"
                return JsonResponse(response, status = 201)
            else:
                response["message"] = "product registration failed"
                return JsonResponse(response, status = 304)

        except NotFoundErr as ne:
            print("reccuring views.product")
            # if name not found error occurs try again
            return product(request)

        except ValueError as v:
            print(v)
            response["message"] = f"{v}"
            return JsonResponse(response, status = 500)

@csrf_exempt
def users(request):
    if (request.method == "GET"):
        response = {}
        body_unicode = request.body.decode("utf-8")

        try:
            creds = {}
            try:
                creds = json.loads(body_unicode)
            except ValueError:
                queryDictUnParsed = request.META["QUERY_STRING"]
                queryDict = QueryDict(queryDictUnParsed)
                creds = queryDict

            status = None

            if (db.isUserValid(creds["username"], creds["pwd"])):
                status = 200
                response["message"] = "USER VALID"
            else:
                status = 403
                response["message"] = "USER NOT VALID"

            return JsonResponse(response, status=status)

        except json.JSONDecodeError as jde:
            response["message"] = jde
            return JsonResponse(response, status=401)
        
        except Exception as e:
            response["message"] = e
            return JsonResponse(response, status = 501)

    if (request.method == "POST"):
        response = {}
    
        try:
            body_unicode = request.body.decode("utf-8")
            creds = json.loads(body_unicode)
            status = None

            if(db.isUserExists(creds["username"]) != True):
                db.registerUser(creds)
                status = 200
                response["message"] = "user succesfully registered"
            else:
                status = 201
                response["message"] = "user already exists"

            return JsonResponse(response, status=status)
        except DatabaseError as de:
            print(de)
            response["message"] = "Database error occured"
            return JsonResponse(response, status=500)
        except KeyError as k:
            print(k)
            response["message"] = f'Json key missing : {k}'
            return JsonResponse(response, status=400)

@csrf_exempt
def usersProduct(request):
    try:
        
        if (request.method == "GET"):
            response = {}
            body_unicode = request.body.decode("utf-8")

            try:
                creds = {}
                try:
                    creds = json.loads(body_unicode)
                except ValueError:
                    queryDictUnParsed = request.META["QUERY_STRING"]
                    queryDict = QueryDict(queryDictUnParsed)
                    creds = queryDict


                if not db.isUserValid(creds["username"], creds["pwd"]):
                    response["message"] = "User Not Valid"
                    return JsonResponse(response, status = 403)
                
                listOfProducts = db.getUsersProducts(creds["username"])

                if(len(listOfProducts) <= 0):
                    response["message"] = "No Products Registered"
                    return JsonResponse(response, status = 204)
                
                listOfDicts = []
                

                for l in listOfProducts:
                    myDict = {}
                    myDict["asin"] = l[0]
                    myDict["name"] = l[1]
                    listOfDicts.append(myDict)
                
                response["message"] = "Products Found"
                response["products"] = listOfDicts

                return JsonResponse(response, status = 200)
            
            except json.JSONDecodeError as jde:
                response["message"] = jde
                return JsonResponse(response, status=401)
            
            except Exception as e:
                response["message"] = e
                return JsonResponse(response, status = 501)

        if request.method == "POST":
            response = {
                "message": "ok"
            }
            try:
                body_unicode = request.body.decode("utf-8")
                print(body_unicode)
                body = json.loads(body_unicode)

                product = utils.getTodaysPrice(body["link"])
                product = json.loads(product)
                
                if (db.isUserValid(body["username"], body["pwd"])):

                    if(db.isUserAndAsinExistInUsersProduct(body["username"], product["asin"]) == True):
                        response["message"] = "user already registered for this product"
                        return JsonResponse(response, status = 201)

                    if (db.isProductExists(product) == False and db.registerProduct(product) == -1):
                        response["message"] = "prouct registration failed"
                        return JsonResponse(response, status = 500)
                    else:
                        db.updateUsersProductTable(body["username"], product["asin"])
                        db.updateFluctuations(product)
                        response["message"] = "product registered succesfully"
                        return JsonResponse(response, status=200)

                else:
                    response["message"] = "user not valid"
                    return JsonResponse(response, status = 401)



            except json.JSONDecodeError as jde:
                print("json.JSONDecodeError error in POST /usersproduct")
                print(jde)
                response["message"] = "jsonDecodeError in POST /views.usersProduct"
                return JsonResponse(response, status = 400)

            except DatabaseError as de:
                print("DatabaseError error in POST /usersproduct")
                print(de)
                response["message"] = f"{de}"
                return JsonResponse(response, 400)
            
            except Exception as e:
                print("Exception error in POST /usersproduct")
                print(e)
                response["message"] = f"{e}"
                return JsonResponse(response, status = 400)

    except Exception as e:
        response = {
            "message": "Something went wrong"
        }
        return JsonResponse(response, status = 500)


        
