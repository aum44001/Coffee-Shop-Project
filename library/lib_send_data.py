from datetime import date, timezone
import datetime
import pymongo
from PyQt5 import QtCore, QtWidgets
Myserver = 'mongodb+srv://Chayapol:aum0825904216@cluster0.xjaok.mongodb.net/<dbname>?retryWrites=true&w=majority'
dataProductlist = []

def clearProduct():
    dataProductlist.clear()

def addDatatoList(data):
    temp = {'size':data[0],
            'price':data[1],
            'qty':data[2]}
    dataProductlist.append(temp)

def editDatatoList(data,pointer):
    temp = {'size': data[0],
            'price': data[1],
            'qty': data[2]}
    dataProductlist[pointer] = temp

def deleteDatainList(pointer):
    del dataProductlist[pointer]

def getDataProducts():
    return dataProductlist

def getLastProductID():
    with (pymongo.MongoClient(Myserver)) as conn:
        db = conn.get_database('Coffee_shop')
        where = {}
        sortz = [("_id",-1)]
        cursor = db.Product.find(where).sort(sortz).limit(1)
        for i in cursor:
            lastID = i['id']
        return  lastID + 1