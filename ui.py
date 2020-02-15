
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
import re
from mongoConnection import MongoConnect

class Ui_MainWindow(object):

    def validateURL(self, url):
        pattern = """^(https?:\\/\\/)?(www\\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\\.)+[\\w]{2,}(\\/\\S*)?$"""
        result = re.match(pattern, url)
        
        return result

    def onSubmitForm(self, status):
        url = self.lineEdit.text()
        valid = self.validateURL(url)
        if (valid):
            print ("Valid url. Yay")
            self.mongo.insertURL(url)
            self.cleanForm()
            self.setURLCheckBoxes()
        else: 
            print ("Nah, bad URL. try again ^_^")
    
    def initMongo(self):
        self.mongo = MongoConnect()
        # initialize database
        self.mongo.initDb()
        
    def cleanForm(self):
        while self.urlForm.count():
            print (self.urlForm.count())
            child = self.urlForm.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def setURLCheckBoxes(self):
        self.mongo.getURLs()
        list = self.mongo.URLlist
        for i,item in enumerate(list):
            name = item.get('name') + 'Label'
            
            tempLabel = QtWidgets.QLabel(self.formLayoutWidget)
            tempLabel.setObjectName(name)
            self.urlForm.setWidget((i+1), QtWidgets.QFormLayout.LabelRole, tempLabel)
            tempLabel.setText(item.get('url'))
            exec("self." + name + " = tempLabel")

            name = item.get('name') + 'CheckBox'
            
            tempCheckbox = QtWidgets.QCheckBox(self.formLayoutWidget)
            tempCheckbox.setObjectName(name)
            self.urlForm.setWidget((i+1), QtWidgets.QFormLayout.FieldRole, tempCheckbox)
            exec("self." + name + " = tempCheckbox")


    def setupUi(self, MainWindow):
        self.initMongo()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(675, 536)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 751, 431))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.label_5 = QtWidgets.QLabel(self.tab_1)
        self.label_5.setGeometry(QtCore.QRect(50, 30, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.tab_1)
        self.pushButton.setGeometry(QtCore.QRect(60, 80, 141, 41))
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(self.tab_1)
        self.label_6.setGeometry(QtCore.QRect(50, 180, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(410, 0, 271, 41))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(50, 80, 401, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.okURLButton = QtWidgets.QPushButton(self.tab_2)
        self.okURLButton.setGeometry(QtCore.QRect(480, 80, 101, 31))
        self.okURLButton.setObjectName("okURLButton")
        self.okURLButton.clicked.connect(self.onSubmitForm)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(50, 120, 211, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(50, 170, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 210, 401, 151))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.urlForm = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.urlForm.setContentsMargins(0, 0, 0, 0)
        self.urlForm.setObjectName("urlForm")

        # retrieve list of urls
        self.setURLCheckBoxes()
        


        self.deleteButton = QtWidgets.QPushButton(self.tab_2)
        self.deleteButton.setGeometry(QtCore.QRect(480, 330, 101, 31))
        self.deleteButton.setObjectName("deleteButton")
        self.tabWidget.addTab(self.tab_2, "")
        self.emergencyHideButton = QtWidgets.QPushButton(self.centralwidget)
        self.emergencyHideButton.setGeometry(QtCore.QRect(260, 440, 171, 41))
        self.emergencyHideButton.setObjectName("emergencyHideButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 675, 21))
        self.menubar.setObjectName("menubar")
        self.menuAdd_File = QtWidgets.QMenu(self.menubar)
        self.menuAdd_File.setObjectName("menuAdd_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuAdd_File.addSeparator()
        self.menubar.addAction(self.menuAdd_File.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "Select forbidden person Image"))
        self.pushButton.setText(_translate("MainWindow", "Upload Image"))
        self.label_6.setText(_translate("MainWindow", "Forbidden People"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Configure Dangerous People"))
        self.label.setText(_translate("MainWindow", "There is a mysterious pack of ketchup in front of you."))
        self.lineEdit.setText(_translate("MainWindow", "reddit.com"))
        self.okURLButton.setText(_translate("MainWindow", "Ok"))
        self.label_2.setText(_translate("MainWindow", "Add Website URL to hide"))
        self.label_3.setText(_translate("MainWindow", "placeholder"))
        self.label_4.setText(_translate("MainWindow", "Configure URLs"))
        # self.url2Label.setText(_translate("MainWindow", "url2222"))
        # self.url3Label.setText(_translate("MainWindow", "url3"))

        list = self.mongo.URLlist
        for item in list:
            name = item.get('name') + 'Label'
            exec("self." + name + ".setText(_translate(\"MainWindow\", item.get('url')))")

        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Configure Windows"))
        self.emergencyHideButton.setText(_translate("MainWindow", "HIDE!"))
        self.menuAdd_File.setTitle(_translate("MainWindow", "Add File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #ui.initMongo()
    MainWindow.show()
    sys.exit(app.exec_())
