from datetime import datetime
import pymongo
from PyQt5 import QtCore, QtWidgets

Myserver = 'mongodb+srv://Chayapol:aum0825904216@cluster0.xjaok.mongodb.net/<dbname>?retryWrites=true&w=majority'

orderdata = []
invoicedata = []
totalprice = []
invoicehtml = []

def Clearorder():
    orderdata.clear()
    invoicedata.clear()
    totalprice.clear()
    invoicehtml.clear()


def addOrder(name, size, price, typeo, qty, id):
    temp = {
        'name': str(name),
        'size': str(size),
        'price': int(price),
        'qty': int(qty),
        'type': str(typeo),
        'id': int(id)}
    orderdata.append(temp)


def deleteOrder(pointer):
    del orderdata[pointer]


def getOrder():
    return orderdata


def updateQtyPro():
    # print(len(orderdata))
    with (pymongo.MongoClient(Myserver)) as conn:
        for i in orderdata:
            db = conn.get_database('Coffee_shop')
            where = {'$and': [{'id': i['id']}, {'products.size': i['size']}]}
            setto = {'$inc': {'products.$.qty': -i['qty']}}
            # print(where)
            # print(setto)
            db.Product.update_one(where, setto)


def calPrice():
    totalp = 0
    for i in orderdata:
        totalp += i['price'] * i['qty']
        sump = i['price'] * i['qty']
        temp = {'name': i['name'],
                'size': i['size'],
                'price': i['price'],
                'qty': i['qty'],
                'total': sump,
                'pro_id': i['id']
                }
        invoicedata.append(temp)
    totalprice.append(totalp)



def insertinvoice():
    datenow = datetime.now()
    invoice_id = getLastInvoiceID()
    # print(datenow)
    # print(invoice_id)
    items = []
    for i in invoicedata:
        # print(i)
        temp = {
            'product_id': i['pro_id'],
            'product_name': i['name'],
            'product_size': i['size'],
            'product_price': i['price'],
            'product_qty': i['qty'],
            'product_total': i['total'],
        }
        items.append(temp)
    # print(items)
    # print(totalprice[0])
    invoicehtml.append(invoice_id)
    invoicehtml.append(datenow)
    invoicehtml.append(items)
    invoicehtml.append(totalprice[0])
    print(invoicehtml)
    with (pymongo.MongoClient(Myserver)) as conn:
        db = conn.get_database('Coffee_shop')
        db.Invoice.insert_one({'invoiceID': invoice_id, 'date': datenow,
                               'items': items, 'total': totalprice[0]})

def getLastInvoiceID():
    with (pymongo.MongoClient(Myserver)) as conn:
        db = conn.get_database('Coffee_shop')
        where = {}
        sortz = [("_id", -1)]
        cursor = db.Invoice.find(where).sort(sortz).limit(1)
        res = list(cursor)
        if len(res) == 0:
            return 1
        else:
            for i in res:
                lastID = i['invoiceID']
            return lastID + 1


def getTotalPrice():
    # print(totalprice[0])
    return float(totalprice[0])


def getInvoice():
    return invoicedata

def getInvoiceforPrint():
    return  invoicehtml