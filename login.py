#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from mainwindow import MainWindow
from utils import ErrorUI

class Login(QtGui.QDialog):

    def __init__(self):
        super(Login, self).__init__()
        title = "Login"
        self.setWindowTitle(str(title))
        
        self.layout = QtGui.QGridLayout(self)

        #name input
        self.nameInput = QtGui.QLineEdit('', self)
        self.nameInput.setFixedHeight(30)
        self.layout.addWidget(self.nameInput, 1,0)
        userLabel = QtGui.QLabel('USER:')
        self.layout.addWidget(userLabel, 0, 0)


        #ip input
        self.ipInput = QtGui.QLineEdit('', self)
        self.ipInput.setFixedHeight(30)
        self.layout.addWidget(self.ipInput, 3, 0)
        ipLabel = QtGui.QLabel('HOST:')
        self.layout.addWidget(ipLabel, 2, 0)

        self.portInput = QtGui.QLineEdit('', self)
        self.portInput.setFixedHeight(30)
        self.layout.addWidget(self.portInput, 5, 0)
        portLabel = QtGui.QLabel('PORT:')
        self.layout.addWidget(portLabel, 4, 0)

        #OK buton
        self.okbutton = QtGui.QPushButton(self)
        self.okbutton.setText("Login")
        self.okbutton.setMinimumWidth(50)
        self.okbutton.setMinimumHeight(45)
        self.layout.addWidget(self.okbutton, 3, 1)
        QtCore.QObject.connect(self.okbutton, QtCore.SIGNAL("clicked()"), self.doLogin)


        self.setLayout(self.layout)

    def doLogin(self):
        username = str(self.nameInput.text())
        hostname = str(self.ipInput.text())
        portnumber = str(self.portInput.text())

        if username != "" and username[0:7] != "REMOVE:" and hostname!="" and portnumber!="":
            try:
                self.userMainWindow = MainWindow(username, hostname,portnumber)
                self.accept()
            except Exception as e:
                print e
                self.error = ErrorUI("Error try again later")
            
        else:
            self.error = ErrorUI("All Fields must be set.")

app = QtGui.QApplication(sys.argv)
usernameWindow = Login()
usernameWindow.show()

sys.exit(app.exec_())