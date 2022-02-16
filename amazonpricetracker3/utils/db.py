from ast import Str
import json
import mysql.connector
from dotenv import load_dotenv
from ..product.Product import Product

load_dotenv()

from .utils import getTime

import os

def getDBConnector():
  return mysql.connector.connect(
  host = os.getenv("MYSQL_HOST"),
  user = os.getenv("MYSQL_USERNAME"),
  password = os.getenv("MYSQL_PASSWORD"),
  database = os.getenv("MYSQL_DATABASE")
)

def getFluctuations(asin):
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f"""
    SELECT * FROM FLUCTUATIONS WHERE 
    ASIN = "{asin}" ORDER BY Date DESC ;
  
  """)

  myresult = cursor.fetchall()

  cursor.close()
  mydb.close()
  return myresult

def getProducts():
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM PRODUCT")

  myresult = cursor.fetchall()

  cursor.close()
  mydb.close()
  return myresult

def isTodaysPriceRecorded(asin):
  time = getTime()
  mydb = getDBConnector()
  cursor = mydb.cursor()
  # SELECT sale_price FROM Sales WHERE EXISTS(SELECT * FROM Sales WHERE tax>150)
  cursor.execute(f"SELECT COUNT(ASIN) FROM FLUCTUATIONS WHERE ASIN = '{asin}' AND Date = '{time['date']}' ")
  
  result = cursor.fetchone()
  cursor.close()
  mydb.close()

  return True if result[0] == 1 else False

def updateFluctuations(products):
  mydb = getDBConnector()
  cursor = mydb.cursor()
  time = getTime()

  # if tuple of json objects
  if(type(products) == list or type(products) == tuple): 
    for p in products:

      product = json.loads(p)
      print("updating fluctuation of product with asin :" + product.get('asin'))
      cursor.execute(f"INSERT INTO FLUCTUATIONS (ASIN, Date, Price) VALUES ('{product.get('asin')}', '{time['date']}', '{product.get('price')}')")
      mydb.commit()

  # if Product object 
  elif(type(products) == Product and isTodaysPriceRecorded(products) != True):
    print("updating fluctuation of product with asin :" + products.asin)
    cursor.execute(f"INSERT INTO FLUCTUATIONS (ASIN, Date, Price) VALUES ('{products.asin}', '{time['date']}', '{products.price}')")
    mydb.commit()
  
  # if json object
  elif(isTodaysPriceRecorded(products["asin"]) != True):
    print("updating fluctuation of product with asin :" + products.get('asin'))
    cursor.execute(f"INSERT INTO FLUCTUATIONS (ASIN, Date, Price) VALUES ('{products.get('asin')}', '{time['date']}', '{products.get('price')}')")
    mydb.commit()

  cursor.close()
  mydb.close()
  
  return cursor.rowcount

def isProductExists(product):

  asin = ""

  if type(product) == Product:
    asin = product.get_asin()
  else:
    asin = product["asin"]

  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f'SELECT COUNT(ASIN) FROM PRODUCT WHERE ASIN = "{asin}"')

  result = cursor.fetchone()

  cursor.close()
  mydb.close()

  return False if result[0] == 0 else True

def registerProduct(product):
  mydb = getDBConnector()
  cursor = mydb.cursor()

  asin = ""
  name = ""
  link = ""

  if type(product) == Product:
    asin = product.asin
    name = product.name
    link = product.link
  else:
    asin = product["asin"]
    name = product["name"]
    link = product["link"]

  cursor.execute(f'INSERT INTO PRODUCT VALUES ( "{asin}", "{name}", "{link}" )')
  mydb.commit()

  cursor.close()
  mydb.close()

  updateFluctuations(product)

  return cursor.rowcount

def getFluctuationsNotRecordedOn(date):
  mydb = getDBConnector()
  cursor = mydb.cursor()
  cursor.execute(f"""
      SELECT PRODUCT.ASIN, PRODUCT.Name, PRODUCT.Link 
      FROM PRODUCT WHERE 
      PRODUCT.ASIN != 
      ALL(SELECT FLUCTUATIONS.ASIN 
          FROM FLUCTUATIONS 
          WHERE Date = '{date}'
        );
  """)

  results = cursor.fetchall()
  cursor.close()
  mydb.close()

  return -1 if len(results) <= 0 else results

def isUserExists(username):
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f'SELECT COUNT(*) FROM USERS WHERE UserName = "{username}"')

  result = cursor.fetchone()
  
  cursor.close()
  mydb.close()

  return True if result[0] == 1 else False

def registerUser(creds):
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f'INSERT INTO USERS(UserName, PWD) VALUES ("{creds["username"]}", "{creds["pwd"]}");')

  mydb.commit()

  cursor.close()
  mydb.close()

  return cursor.rowcount

def isUserValid(username, pwd):
  # SELECT EXISTS(SELECT * FROM USERS WHERE UserName = "perrytheplatypus" AND PWD = "12345678")
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f'SELECT EXISTS(SELECT * FROM USERS WHERE UserName = "{username}" AND PWD = "{pwd}")')

  result = cursor.fetchone()

  cursor.close()
  mydb.close()

  return True if result[0] == 1 else False

def updateUsersProductTable(username, asin):
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f"""
    INSERT INTO USERSPRODUCT (UserName, ASIN)
    VALUES (
        "{username}",
        "{asin}"
    );
  """)

  mydb.commit()

  cursor.close()
  mydb.close()

  return cursor.rowcount

def isUserAndAsinExistInUsersProduct(username, asin):
  mydb = getDBConnector()
  cursor = mydb.cursor()

  cursor.execute(f"""
    SELECT EXISTS(SELECT * FROM USERSPRODUCT WHERE UserName = "{username}" AND ASIN = "{asin}");
  """)

  result = cursor.fetchone()

  cursor.close()
  mydb.close()

  return False if result[0] == 0 else True

def getUsersProducts(username):
  mydb = getDBConnector()
  cursor = mydb.cursor()
  cursor.execute(f"""
      SELECT PRODUCT.ASIN, PRODUCT.Name FROM PRODUCT, 
      USERSPRODUCT WHERE PRODUCT.ASIN = USERSPRODUCT.ASIN 
      AND USERSPRODUCT.UserName = "{username}";
  """)

  results = cursor.fetchall()
  cursor.close()
  mydb.close()

  return results