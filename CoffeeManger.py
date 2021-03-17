# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeManger.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import ctypes
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM = 0x30
ICON_INFO = 0x40
ICON_STOP = 0x10
import pymongo
import re
from PyQt5.QtWidgets import QTableWidgetItem
from Insert_Edit import Ui_Insert_Edit
from library.lib_query_datatable import currId,Cleardata
from library.lib_send_data import clearProduct


Myserver = 'mongodb+srv://Chayapol:aum0825904216@cluster0.xjaok.mongodb.net/<dbname>?retryWrites=true&w=majority'


class Ui_ShowDataManager(object):

    def toInsert(self):
        status = " Add new product"
        title = "Data Insert"
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Insert_Edit()
        self.ui.setupUi(self.window,status,title)
        self.window.exec_()
        clearProduct()
        Cleardata()
        self.display({})


    def toEdit(self):
        currtb = self.tb_Showdata.item(self.tb_Showdata.currentRow(),0)
        if str(currtb) == "None":
            ctypes.windll.user32.MessageBoxW(0, "Please select data in table!!", "Warning", ICON_EXLAIM | MB_OK)
        else:
            status = " Edit product"
            title = "Data Edit"
            currId(currtb.text())
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Insert_Edit()
            self.ui.setupUi(self.window, status,title)
            self.window.exec_()
            Cleardata()
            clearProduct()
            self.display({})

    def DeleteData(self):
        currtb = self.tb_Showdata.item(self.tb_Showdata.currentRow(), 0)
        if str(currtb) == "None":
            ctypes.windll.user32.MessageBoxW(0, "Please select data in table!!", "Warning", ICON_EXLAIM | MB_OK)
        else:
            check = ctypes.windll.user32.MessageBoxW(0, "Are you sure to delete data id = {} ??".format(currtb.text()), "Warning", ICON_EXLAIM | MB_YESNO)
            if check == 6:
                with pymongo.MongoClient(Myserver) as conn:
                    db = conn.get_database('Coffee_shop')
                    where = {'id': int(currtb.text())}
                    db.Product.delete_one(where)
                ctypes.windll.user32.MessageBoxW(0, "Your product has been delete successfully!!", "Warning", ICON_INFO | MB_OK)

        self.display({})


    def checkLogout(self):
        check = ctypes.windll.user32.MessageBoxW(0, "Are you sure to Log-out ??", "Warning", ICON_EXLAIM | MB_YESNO)
        if check == 6:
            self.toHome()

    def toHome(self):
        self.thiswindow.close()
        self.Home.show()

    def checkonlynum(self,txt):
        check = re.search("^[0-9]*$", txt)
        if (check):
            return True
        else:
            return False

    def setCondition(self):
        inputt = self.txt_Search.toPlainText()
        colselect = self.cbo_Doc_Search.currentText()
        if colselect == "Id =":
            if self.checkonlynum(inputt):
                mycondi = {"id": int(inputt)}
                self.display(mycondi)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Please enter number only!!", "Warning", ICON_EXLAIM | MB_OK)
        elif colselect == "Name":
            mycondi = {"name": {"$regex": inputt}}
            self.display(mycondi)
        elif colselect == "Size":
            mycondi = {"products.size": {"$regex": inputt}}
            self.display(mycondi)
        elif colselect == "Price >=":
            if self.checkonlynum(inputt):
                mycondi = {"products.price": {"$gte": int(inputt)}}
                self.display(mycondi)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Please enter number only!!", "Warning", ICON_EXLAIM | MB_OK)
        elif colselect == "Price <=":
            if self.checkonlynum(inputt):
                mycondi = {"products.price": {"$lte": int(inputt)}}
                self.display(mycondi)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Please enter number only!!", "Warning", ICON_EXLAIM | MB_OK)
        elif colselect == "Stock >=":
            if self.checkonlynum(inputt):
                mycondi = {"products.qty": {"$gte": int(inputt)}}
                self.display(mycondi)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Please enter number only!!", "Warning", ICON_EXLAIM | MB_OK)
        elif colselect == "Stock <=":
            if self.checkonlynum(inputt):
                mycondi = {"products.qty": {"$lte": int(inputt)}}
                self.display(mycondi)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Please enter number only!!", "Warning", ICON_EXLAIM | MB_OK)
        elif colselect == "Type":
            mycondi = {"type": {'$regex': inputt}}
            self.display(mycondi)
        elif colselect == "Blend":
            mycondi = {"blend": {'$regex': inputt}}
            self.display(mycondi)
        else:
            mycondi = {}
            self.display(mycondi)



    def display(self, condition):
        with pymongo.MongoClient(Myserver) as conn:
            db = conn.get_database('Coffee_shop')
            where = condition
            read = db.Product.find(where)
            cursor = db.Product.find(where)
            count = db.Product.count_documents(where)
            rowcount = 0
            for i in read:
                for j in range(len(i['products'])):
                    rowcount += 1

            ## Table Widget
            self.tb_Showdata.setRowCount(rowcount)
            self.tb_Showdata.setColumnCount(10)

            header = self.tb_Showdata.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)

            header1 = QtWidgets.QTableWidgetItem("Id")
            header2 = QtWidgets.QTableWidgetItem("Name")
            header3 = QtWidgets.QTableWidgetItem("Size")
            header4 = QtWidgets.QTableWidgetItem("Price")
            header5 = QtWidgets.QTableWidgetItem("Stock")
            header6 = QtWidgets.QTableWidgetItem("Type")
            header7 = QtWidgets.QTableWidgetItem("Blend")
            header8 = QtWidgets.QTableWidgetItem("Aroma")
            header9 = QtWidgets.QTableWidgetItem("Roasting_Lvl")
            header10 = QtWidgets.QTableWidgetItem("Aftertaste")

            self.tb_Showdata.setHorizontalHeaderItem(0, header1)
            self.tb_Showdata.setHorizontalHeaderItem(1, header2)
            self.tb_Showdata.setHorizontalHeaderItem(2, header3)
            self.tb_Showdata.setHorizontalHeaderItem(3, header4)
            self.tb_Showdata.setHorizontalHeaderItem(4, header5)
            self.tb_Showdata.setHorizontalHeaderItem(5, header6)
            self.tb_Showdata.setHorizontalHeaderItem(6, header7)
            self.tb_Showdata.setHorizontalHeaderItem(7, header8)
            self.tb_Showdata.setHorizontalHeaderItem(8, header9)
            self.tb_Showdata.setHorizontalHeaderItem(9, header10)

            row = 0
            for i in cursor:
                for j in range(len(i['products'])):
                    self.tb_Showdata.setItem(row, 0, QTableWidgetItem('{}'.format(i['id'])))
                    self.tb_Showdata.setItem(row, 1, QTableWidgetItem('{}'.format(i['name'])))
                    self.tb_Showdata.setItem(row, 2, QTableWidgetItem('{}'.format(i['products'][j]['size'])))
                    self.tb_Showdata.setItem(row, 3, QTableWidgetItem('{}'.format(i['products'][j]['price'])))
                    self.tb_Showdata.setItem(row, 4, QTableWidgetItem('{}'.format(i['products'][j]['qty'])))
                    self.tb_Showdata.setItem(row, 5, QTableWidgetItem('{}'.format(i['type'])))
                    self.tb_Showdata.setItem(row, 6, QTableWidgetItem('{}'.format(i['blend'])))
                    self.tb_Showdata.setItem(row, 7, QTableWidgetItem('{}'.format(i['aroma'])))
                    self.tb_Showdata.setItem(row, 8, QTableWidgetItem('{}'.format(i['roastinglvl'])))
                    self.tb_Showdata.setItem(row, 9, QTableWidgetItem('{}'.format(i['aftertaste'])))
                    row += 1

            self.lb_Found.setText(" Found {} Record".format(count))

    # add Home param before to complete project
    def setupUi(self, ShowDataManager, Home, name):

        ShowDataManager.setObjectName("ShowDataManager")
        ShowDataManager.resize(1016, 549)
        ShowDataManager.setStyleSheet("background-color:#B99C8B;")
        self.lb_username = QtWidgets.QLabel(ShowDataManager)
        self.lb_username.setGeometry(QtCore.QRect(20, 20, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.lb_username.setFont(font)
        self.lb_username.setStyleSheet("background-color:#755F55;\n"
                                       "border:1px;\n"
                                       "border-radius: 8px;\n"
                                       "color:white;")
        self.lb_username.setObjectName("lb_username")
        self.btn_Insert = QtWidgets.QPushButton(ShowDataManager)
        self.btn_Insert.setGeometry(QtCore.QRect(680, 70, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Insert.setFont(font)
        self.btn_Insert.setStyleSheet("background-color:#755F55;\n"
                                      "color:white;")
        self.btn_Insert.setObjectName("btn_Insert")
        self.btn_Edit = QtWidgets.QPushButton(ShowDataManager)
        self.btn_Edit.setGeometry(QtCore.QRect(790, 70, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Edit.setFont(font)
        self.btn_Edit.setStyleSheet("background-color:#755F55;\n"
                                    "color:white;")
        self.btn_Edit.setObjectName("btn_Edit")
        self.tb_Showdata = QtWidgets.QTableWidget(ShowDataManager)
        self.tb_Showdata.setGeometry(QtCore.QRect(20, 110, 971, 401))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.tb_Showdata.setFont(font)
        self.tb_Showdata.setStyleSheet("background-color:white;")
        self.tb_Showdata.setObjectName("tb_Showdata")
        self.tb_Showdata.setColumnCount(0)

        self.tb_Showdata.setRowCount(0)
        self.tb_Showdata.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tb_Showdata.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


        self.txt_Search = QtWidgets.QTextEdit(ShowDataManager)
        self.txt_Search.setGeometry(QtCore.QRect(310, 70, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.txt_Search.setFont(font)
        self.txt_Search.setStyleSheet("background-color:white;")
        self.txt_Search.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txt_Search.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txt_Search.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.txt_Search.setObjectName("txt_Search")

        # combobox
        self.cbo_Doc_Search = QtWidgets.QComboBox(ShowDataManager)
        self.cbo_Doc_Search.setGeometry(QtCore.QRect(110, 70, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.cbo_Doc_Search.setFont(font)
        self.cbo_Doc_Search.setStyleSheet("background-color:white;")
        self.cbo_Doc_Search.setObjectName("cbo_Doc_Search")
        self.cbo_Doc_Search.addItem("Select All")
        self.cbo_Doc_Search.addItem("Id =")
        self.cbo_Doc_Search.addItem("Name")
        self.cbo_Doc_Search.addItem("Size")
        self.cbo_Doc_Search.addItem("Price >=")
        self.cbo_Doc_Search.addItem("Price <=")
        self.cbo_Doc_Search.addItem("Stock >=")
        self.cbo_Doc_Search.addItem("Stock <=")
        self.cbo_Doc_Search.addItem("Type")
        self.cbo_Doc_Search.addItem("Blend")

        self.label_2 = QtWidgets.QLabel(ShowDataManager)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_2.setObjectName("label_2")
        self.btn_Delete = QtWidgets.QPushButton(ShowDataManager)
        self.btn_Delete.setGeometry(QtCore.QRect(900, 70, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Delete.setFont(font)
        self.btn_Delete.setStyleSheet("background-color:#755F55;\n"
                                      "color:white;")
        self.btn_Delete.setObjectName("btn_Delete")
        self.btn_Logout = QtWidgets.QPushButton(ShowDataManager)
        self.btn_Logout.setGeometry(QtCore.QRect(900, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Logout.setFont(font)
        self.btn_Logout.setStyleSheet("background-color:#755F55;\n"
                                      "color:white;")
        self.btn_Logout.setObjectName("btn_Logout")
        self.btn_Search = QtWidgets.QPushButton(ShowDataManager)
        self.btn_Search.setGeometry(QtCore.QRect(570, 70, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Search.setFont(font)
        self.btn_Search.setStyleSheet("background-color:#755F55;\n"
                                      "color:white;")
        self.btn_Search.setObjectName("btn_Search")
        self.lb_Found = QtWidgets.QLabel(ShowDataManager)
        self.lb_Found.setGeometry(QtCore.QRect(250, 20, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.lb_Found.setFont(font)
        self.lb_Found.setStyleSheet("background-color:#755F55;\n"
                                    "border:1px;\n"
                                    "border-radius: 8px;\n"
                                    "color:white;")
        self.lb_Found.setObjectName("lb_Found")

        # button click
        self.btn_Logout.clicked.connect(self.checkLogout)
        self.btn_Search.clicked.connect(self.setCondition)
        self.btn_Insert.clicked.connect(self.toInsert)
        self.btn_Edit.clicked.connect(self.toEdit)
        self.btn_Delete.clicked.connect(self.DeleteData)

        # uncomment before complete project
        self.thiswindow = ShowDataManager
        self.Home = Home

        self.display({})

        self.retranslateUi(ShowDataManager, name)
        QtCore.QMetaObject.connectSlotsByName(ShowDataManager)



    def retranslateUi(self, ShowDataManager, name):
        _translate = QtCore.QCoreApplication.translate
        ShowDataManager.setWindowTitle(_translate("ShowDataManager", "Coffee Management"))
        self.lb_username.setText(_translate("ShowDataManager", " Welcome " + name))
        self.btn_Insert.setText(_translate("ShowDataManager", "Insert"))
        self.btn_Edit.setText(_translate("ShowDataManager", "Edit"))
        self.label_2.setText(_translate("ShowDataManager", " Search By"))
        self.btn_Delete.setText(_translate("ShowDataManager", "Delete"))
        self.btn_Logout.setText(_translate("ShowDataManager", "Logout"))
        self.btn_Search.setText(_translate("ShowDataManager", "Search"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ShowDataManager = QtWidgets.QDialog()
    ui = Ui_ShowDataManager()
    ui.setupUi(ShowDataManager)
    ShowDataManager.show()
    sys.exit(app.exec_())