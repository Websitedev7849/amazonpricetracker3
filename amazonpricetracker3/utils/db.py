import json
import mysql.connector
from dotenv import load_dotenv
from ..product.Product import Product

load_dotenv()

from .utils import getTime

import os
mydb = mysql.connector.connect(
  host = os.getenv("MYSQL_HOST"),
  user = os.getenv("MYSQL_USERNAME"),
  password = os.getenv("MYSQL_PASSWORD"),
  database = os.getenv("MYSQL_DATABASE")
)

def getFluctuations():
  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM FLUCTUATIONS")

  myresult = cursor.fetchall()

  cursor.close()
  
  return myresult

def getProducts():
  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM PRODUCT")

  myresult = cursor.fetchall()

  cursor.close()

  return myresult

def isTodaysPriceRecorded(asin):
  time = getTime()
  cursor = mydb.cursor()
  # SELECT sale_price FROM Sales WHERE EXISTS(SELECT * FROM Sales WHERE tax>150)
  cursor.execute(f"SELECT COUNT(ASIN) FROM FLUCTUATIONS WHERE ASIN = '{asin}' AND Date = '{time['date']}' ")
  
  result = cursor.fetchone()
  cursor.close()

  return True if result[0] == 1 else False

def updateFluctuations(products):
  cursor = mydb.cursor()
  time = getTime()

  if(type(products) == list or type(products) == tuple):
    for p in products:

      product = json.loads(p)

      cursor.execute(f"INSERT INTO FLUCTUATIONS (ASIN, Date, Price) VALUES ('{product.get('asin')}', '{time['date']}', '{product.get('price')}')")
      mydb.commit()
        
  elif(type(products) == Product and isTodaysPriceRecorded(products) != True):
    cursor.execute(f"INSERT INTO FLUCTUATIONS (ASIN, Date, Price) VALUES ('{products.get_asin()}', '{time['date']}', '{products.getPrice()}')")
    mydb.commit()

  cursor.close()
  
  return cursor.rowcount

def isProductExists(product):
  cursor = mydb.cursor()

  cursor.execute(f'SELECT COUNT(ASIN) FROM PRODUCT WHERE ASIN = "{product.get_asin()}"')

  result = cursor.fetchone()

  cursor.close()

  return False if result[0] == 0 else True

def registerProduct(product):
  cursor = mydb.cursor()

  cursor.execute(f'INSERT INTO PRODUCT VALUES ( "{product.get_asin()}", "{product.getName()}", "{product.getLink()}" )')
  mydb.commit()

  cursor.close()

  updateFluctuations(product)

  return cursor.rowcount

def getFluctuationsNotRecordedOn(date):
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
  return -1 if len(results) <= 0 else results
