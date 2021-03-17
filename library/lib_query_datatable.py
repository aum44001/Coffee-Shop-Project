from datetime import date, timezone
import datetime
import pymongo
from PyQt5 import QtCore, QtWidgets
Myserver = 'mongodb+srv://Chayapol:aum0825904216@cluster0.xjaok.mongodb.net/<dbname>?retryWrites=true&w=majority'

currid = []
currdata = []
currpro = []

def Clearcurrpro():
    currpro.clear()

def Cleardata():
    currid.clear()
    currdata.clear()

def addcurrPro(data):
    currpro.append(data[0])
    currpro.append(data[1])
    currpro.append(data[2])
    currpro.append(data[3])

def getcurrPro():
    return currpro

def currId(cid):
    currid.append(int(cid))

def querrycurrData():
    with (pymongo.MongoClient(Myserver)) as conn:
        db = conn.get_database('Coffee_shop')
        where = {"id":currid[0]}
        cursor = db.Product.find(where)
        for i in cursor:
                currdata.append(i["id"])
                currdata.append(i["name"])
                currdata.append(i["products"])
                currdata.append(i["type"])
                currdata.append(i["blend"])
                currdata.append(i["aroma"])
                currdata.append(i["roastinglvl"])
                currdata.append(i["aftertaste"])
        # print(currdata)
        return currdata