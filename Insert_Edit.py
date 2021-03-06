# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Insert_Edit.ui'
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
Myserver = 'mongodb+srv://Chayapol:aum0825904216@cluster0.xjaok.mongodb.net/<dbname>?retryWrites=true&w=majority'
import pymongo
from Insert_Inproduct import Ui_Insert_Inproduct
from library.lib_send_data import getDataProducts,getLastProductID,addDatatoList,deleteDatainList
from library.lib_query_datatable import querrycurrData,addcurrPro,getcurrPro,Clearcurrpro


class Ui_Insert_Edit(object):

    def toAddproducts(self):
        # print("Add Ja")
        select = self.tb_Products.item(self.tb_Products.currentRow(), 0)
        if str(select) == "None":
            status = "Add"
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Insert_Inproduct()
            self.ui.setupUi(self.window,status)

            self.window.exec_()
            self.showDataProduct(getDataProducts())
        else:
            self.toEditproducts()

    def toEditproducts(self):
        # print("Edit Ja")
        status = "Edit"
        temp = []
        pointer = self.tb_Products.currentRow()
        size = self.tb_Products.item(self.tb_Products.currentRow(), 0).text()
        price = self.tb_Products.item(self.tb_Products.currentRow(), 1).text()
        qty = self.tb_Products.item(self.tb_Products.currentRow(), 2).text()
        # print(pointer)
        temp.append(size)
        temp.append(price)
        temp.append(qty)
        temp.append(pointer)
        addcurrPro(temp)

        self.window = QtWidgets.QDialog()
        self.ui = Ui_Insert_Inproduct()
        self.ui.setupUi(self.window, status)

        self.window.exec_()
        Clearcurrpro()
        print(getDataProducts())
        self.showDataProduct(getDataProducts())

    def toDeleteproducts(self):

        pointer = self.tb_Products.currentRow()
        # print(pointer)
        if pointer == -1:
            ctypes.windll.user32.MessageBoxW(0, "Please select data to Delete!!", "Warning", ICON_EXLAIM | MB_OK)
        else:
            check = ctypes.windll.user32.MessageBoxW(0, "Are you sure to delete row {}!!".format(pointer+1), "Warning", ICON_EXLAIM | MB_YESNO)
            if check == 6 :
                deleteDatainList(pointer)
                Clearcurrpro()
            self.showDataProduct(getDataProducts())

    def showDataProduct(self, inputProduct):
        self.tb_Products.setRowCount(0)
        countitem = 0
        for rowdata in inputProduct:
            self.tb_Products.insertRow(countitem)
            countcol = 0
            for data in rowdata.values():
                self.tb_Products.setItem(countitem, countcol, QtWidgets.QTableWidgetItem('{}'.format(data)))
                countcol += 1
            countitem += 1

    def insertProduct(self):
        pid = int(self.txt_Id.text())
        pname = self.txt_Name.text()
        ptype = self.cbo_Type.currentText()
        pblend = self.cbo_Blend.currentText()
        paroma = self.txt_Aroma.text()
        prosted = self.cbo_Roasted.currentText()
        ptaste = self.txt_Taste.text()
        products = getDataProducts()
        if pname == "" and products == []:
            ctypes.windll.user32.MessageBoxW(0, "Please Enter product name,size,price and stock", "Warning",
                                             ICON_EXLAIM|MB_OK)
        elif pname == "":
            ctypes.windll.user32.MessageBoxW(0, "Please Enter product name", "Warning",
                                             ICON_EXLAIM | MB_OK)
        elif products == []:
            ctypes.windll.user32.MessageBoxW(0, "Please Enter size,price and stock", "Warning",
                                             ICON_EXLAIM | MB_OK)
        else:
            with (pymongo.MongoClient(Myserver)) as conn:
                db = conn.get_database('Coffee_shop')
                db.Product.insert_one({'id': pid, 'name': pname,
                                                    'products': products, 'type': ptype,
                                                    'blend': pblend, 'aroma': paroma,
                                                    'roastinglvl': prosted, 'aftertaste': ptaste})
                ctypes.windll.user32.MessageBoxW(0, "Insert New Product Complete!!", "Infomation",
                                                 ICON_INFO | MB_OK)
                self.thiswindow.close()

    def checkcurrindexRoasted(self,data):
        if data == "Ex Light":
            return 0
        elif data == "Light":
            return 1
        elif data == "Medium":
            return 2
        elif data == "Dark":
            return 3
        elif data == "Ex Dark":
            return 4
        else:
            return 0

    def checkcurrindexBlend(self,data):
        if data == "Arabica":
            return 0
        elif data == "Robusta":
            return 1
        elif data == "Excelsa":
            return 2
        elif data == "Liberica":
            return 3
        else:
            return 0

    def checkcurrindexType(self,data):
        if data == "Classic":
            return 0
        elif data == "Espresso":
            return 1
        elif data == "Cappuccino":
            return 2
        elif data == "Latte":
            return 3
        elif data == "Mocha":
            return 4
        elif data == "Americano":
            return 5
        elif data == "Special":
            return 6
        else:
            return 0

    def editProduct(self):
        pid = int(self.txt_Id.text())
        pname = self.txt_Name.text()
        ptype = self.cbo_Type.currentText()
        pblend = self.cbo_Blend.currentText()
        paroma = self.txt_Aroma.text()
        prosted = self.cbo_Roasted.currentText()
        ptaste = self.txt_Taste.text()
        products = getDataProducts()
        if pname == "" and products == []:
            ctypes.windll.user32.MessageBoxW(0, "Please Enter product name,size,price and stock", "Warning",
                                             ICON_EXLAIM | MB_OK)
        elif pname == "":
            ctypes.windll.user32.MessageBoxW(0, "Please Enter product name", "Warning",
                                             ICON_EXLAIM | MB_OK)
        elif products == []:
            ctypes.windll.user32.MessageBoxW(0, "Please Enter size,price and stock", "Warning",
                                             ICON_EXLAIM | MB_OK)
        else:
            with pymongo.MongoClient(Myserver) as conn:
                db = conn.get_database('Coffee_shop')
                where = {'id': pid}
                setto = {'$set': {'name': pname,
                         'products': products,
                         'type': ptype,
                         'blend': pblend,
                         'aroma': paroma,
                         'roastinglvl': prosted,
                         'aftertaste': ptaste}}
                db.Product.update_many(where, setto)

            ctypes.windll.user32.MessageBoxW(0, "Edit Product Complete!!", "Infomation",
                                             ICON_INFO | MB_OK)
            self.thiswindow.close()


    def setupUi(self, Insert_Edit, status,title):
        Insert_Edit.setObjectName("Insert_Edit")
        Insert_Edit.resize(378, 650)
        Insert_Edit.setStyleSheet("background-color:#B99C8B;")
        self.lb_Showstatus = QtWidgets.QLabel(Insert_Edit)
        self.lb_Showstatus.setGeometry(QtCore.QRect(30, 20, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.lb_Showstatus.setFont(font)
        self.lb_Showstatus.setStyleSheet("background-color:#755F55;\n"
                                         "border:1px;\n"
                                         "border-radius: 8px;\n"
                                         "color:white;")
        self.lb_Showstatus.setObjectName("lb_Showstatus")
        self.label_2 = QtWidgets.QLabel(Insert_Edit)
        self.label_2.setGeometry(QtCore.QRect(30, 81, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Insert_Edit)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Insert_Edit)
        self.label_4.setGeometry(QtCore.QRect(30, 180, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Insert_Edit)
        self.label_5.setGeometry(QtCore.QRect(30, 350, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Insert_Edit)
        self.label_6.setGeometry(QtCore.QRect(30, 400, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Insert_Edit)
        self.label_7.setGeometry(QtCore.QRect(30, 450, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Insert_Edit)
        self.label_8.setGeometry(QtCore.QRect(30, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Insert_Edit)
        self.label_9.setGeometry(QtCore.QRect(30, 550, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color:#755F55;\n"
                                   "border:1px;\n"
                                   "border-radius: 8px;\n"
                                   "color:white;")
        self.label_9.setObjectName("label_9")
        self.txt_Id = QtWidgets.QLineEdit(Insert_Edit)
        self.txt_Id.setGeometry(QtCore.QRect(130, 80, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.txt_Id.setFont(font)
        self.txt_Id.setStyleSheet("background-color:white;")
        self.txt_Id.setObjectName("txt_Id")
        self.txt_Id.setText(str(getLastProductID()))
        self.txt_Id.setEnabled(False)


        self.txt_Name = QtWidgets.QLineEdit(Insert_Edit)
        self.txt_Name.setGeometry(QtCore.QRect(130, 130, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.txt_Name.setFont(font)
        self.txt_Name.setStyleSheet("background-color:white;")
        self.txt_Name.setObjectName("txt_Name")
        self.txt_Aroma = QtWidgets.QLineEdit(Insert_Edit)
        self.txt_Aroma.setGeometry(QtCore.QRect(130, 450, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.txt_Aroma.setFont(font)
        self.txt_Aroma.setStyleSheet("background-color:white;")
        self.txt_Aroma.setObjectName("txt_Aroma")
        self.txt_Taste = QtWidgets.QLineEdit(Insert_Edit)
        self.txt_Taste.setGeometry(QtCore.QRect(130, 550, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.txt_Taste.setFont(font)
        self.txt_Taste.setStyleSheet("background-color:white;")
        self.txt_Taste.setObjectName("txt_Taste")
        self.btn_Save = QtWidgets.QPushButton(Insert_Edit)
        self.btn_Save.setGeometry(QtCore.QRect(250, 600, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Save.setFont(font)
        self.btn_Save.setStyleSheet("background-color:#755F55;\n"
                                    "color:white;")
        self.btn_Save.setObjectName("btn_Save")
        self.btn_Addproduct = QtWidgets.QPushButton(Insert_Edit)
        self.btn_Addproduct.setGeometry(QtCore.QRect(190, 180, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Addproduct.setFont(font)
        self.btn_Addproduct.setStyleSheet("background-color:#755F55;\n"
                                          "color:white;")
        self.btn_Addproduct.setObjectName("btn_Addproduct")
        self.tb_Products = QtWidgets.QTableWidget(Insert_Edit)
        self.tb_Products.setGeometry(QtCore.QRect(30, 230, 311, 101))

        self.btn_Deleteproduct = QtWidgets.QPushButton(Insert_Edit)
        self.btn_Deleteproduct.setGeometry(QtCore.QRect(270, 180, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.btn_Deleteproduct.setFont(font)
        self.btn_Deleteproduct.setStyleSheet("background-color:#755F55;\n"
                                             "color:white;")
        self.btn_Deleteproduct.setObjectName("btn_Deleteproduct")


        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.tb_Products.setFont(font)
        self.tb_Products.setStyleSheet("background-color:white;")
        self.tb_Products.setObjectName("tb_Products")
        self.tb_Products.setRowCount(0)
        self.tb_Products.setColumnCount(3)

        header = self.tb_Products.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)

        header1 = QtWidgets.QTableWidgetItem("Size")
        header2 = QtWidgets.QTableWidgetItem("Price")
        header3 = QtWidgets.QTableWidgetItem("Stock")

        self.tb_Products.setHorizontalHeaderItem(0, header1)
        self.tb_Products.setHorizontalHeaderItem(1, header2)
        self.tb_Products.setHorizontalHeaderItem(2, header3)

        self.tb_Products.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tb_Products.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # combobox zone
        self.cbo_Type = QtWidgets.QComboBox(Insert_Edit)
        self.cbo_Type.setGeometry(QtCore.QRect(130, 350, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.cbo_Type.setFont(font)
        self.cbo_Type.setStyleSheet("background-color:white;")
        self.cbo_Type.setObjectName("cbo_Type")
        self.cbo_Type.addItem("Classic")
        self.cbo_Type.addItem("Espresso")
        self.cbo_Type.addItem("Cappuccino")
        self.cbo_Type.addItem("Latte")
        self.cbo_Type.addItem("Mocha")
        self.cbo_Type.addItem("Americano")
        self.cbo_Type.addItem("Special")

        self.cbo_Blend = QtWidgets.QComboBox(Insert_Edit)
        self.cbo_Blend.setGeometry(QtCore.QRect(130, 400, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.cbo_Blend.setFont(font)
        self.cbo_Blend.setStyleSheet("background-color:white;")
        self.cbo_Blend.setObjectName("cbo_Blend")
        self.cbo_Blend.addItem("Arabica")
        self.cbo_Blend.addItem("Robusta")
        self.cbo_Blend.addItem("Excelsa")
        self.cbo_Blend.addItem("Liberica")


        self.cbo_Roasted = QtWidgets.QComboBox(Insert_Edit)
        self.cbo_Roasted.setGeometry(QtCore.QRect(130, 500, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Kanit Light")
        font.setPointSize(12)
        self.cbo_Roasted.setFont(font)
        self.cbo_Roasted.setStyleSheet("background-color:white;")
        self.cbo_Roasted.setObjectName("cbo_Roasted")
        self.cbo_Roasted.addItem("Ex Light")
        self.cbo_Roasted.addItem("Light")
        self.cbo_Roasted.addItem("Medium")
        self.cbo_Roasted.addItem("Dark")
        self.cbo_Roasted.addItem("Ex Dark")

        # set curr index select by table data to show in edit
        if(status == " Edit product"):
            Insert_Edit.setWindowTitle("Data Edit")
            data = querrycurrData()
            self.txt_Id.setText(str(data[0]))
            self.txt_Name.setText(data[1])
            for i in data[2]:
                temp = []
                temp.append(i['size'])
                temp.append(i['price'])
                temp.append(i['qty'])
                addDatatoList(temp)
            self.showDataProduct(getDataProducts())
            self.cbo_Type.setCurrentIndex(self.checkcurrindexType(data[3]))
            self.cbo_Blend.setCurrentIndex(self.checkcurrindexBlend(data[4]))
            self.txt_Aroma.setText(data[5])
            self.cbo_Roasted.setCurrentIndex(self.checkcurrindexRoasted(data[6]))
            self.txt_Taste.setText(data[7])

        # button click
        self.btn_Addproduct.clicked.connect(self.toAddproducts)
        if status == " Add new product":
            self.btn_Save.clicked.connect(self.insertProduct)
        else:
            self.btn_Save.clicked.connect(self.editProduct)
        self.btn_Deleteproduct.clicked.connect(self.toDeleteproducts)

        self.thiswindow = Insert_Edit

        self.retranslateUi(Insert_Edit, status,title)
        QtCore.QMetaObject.connectSlotsByName(Insert_Edit)

    def retranslateUi(self, Insert_Edit, status,title):
        _translate = QtCore.QCoreApplication.translate
        Insert_Edit.setWindowTitle(_translate("Insert_Edit", title))
        self.lb_Showstatus.setText(_translate("Insert_Edit", status))
        self.label_2.setText(_translate("Insert_Edit", " Id"))
        self.label_3.setText(_translate("Insert_Edit", " Name"))
        self.label_4.setText(_translate("Insert_Edit", " Products"))
        self.label_5.setText(_translate("Insert_Edit", " Type"))
        self.label_6.setText(_translate("Insert_Edit", " Blend"))
        self.label_7.setText(_translate("Insert_Edit", " Aroma"))
        self.label_8.setText(_translate("Insert_Edit", " Roastinglvl"))
        self.label_9.setText(_translate("Insert_Edit", " Aftertaste"))
        self.btn_Save.setText(_translate("Insert_Edit", "Save"))
        self.btn_Addproduct.setText(_translate("Insert_Edit", "Add"))
        self.btn_Deleteproduct.setText(_translate("Insert_Edit","Delete"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Insert_Edit = QtWidgets.QDialog()
    ui = Ui_Insert_Edit()
    ui.setupUi(Insert_Edit)
    Insert_Edit.show()
    sys.exit(app.exec_())
