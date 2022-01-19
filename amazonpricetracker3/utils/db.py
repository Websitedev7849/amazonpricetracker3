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
  mycursor = mydb.cursor()

  mycursor.execute("SELECT * FROM FLUCTUATIONS")

  myresult = mycursor.fetchall()
  
  return myresult

def getProducts():
  mycursor = mydb.cursor()

  mycursor.execute("SELECT * FROM PRODUCT")

  myresult = mycursor.fetchall()
  
  return myresult

def isTodaysPriceRecorded(asin):
  time = getTime()
  cursor = mydb.cursor()
  cursor.execute(f"SELECT COUNT(ASIN) FROM FLUCTUATIONS WHERE ASIN = '{asin}' AND Date = '{time['date']}' ")
  
  result = cursor.fetchone()

  return True if result[0] == 1 else False

def getTodaysPrice(asin):

    product = Product(f"https://www.amazon.in/dp/{asin}")
    print(product.toString())

    """
    Done: check if asin with products asin exists in fluctuations table
    remember exception handling
    if not register price
    """
