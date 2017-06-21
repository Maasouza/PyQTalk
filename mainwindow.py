import sys
from PyQt4 import QtCore, QtGui
from client import *
from utils import *
from userserver import *
import random



class MainWindow(QtGui.QDialog):

    def chatStarted(self):
        clickedItem = self.list.currentItem()
        if clickedItem != None:
            user = str(self.list.currentItem().text())
            ip = self.userList[user]
            print ip
            if ip != None:
                chat = Chat(self.username, user, ip)
                self.chats[user] = chat

    def receivedMessage(self, data):
        message = Message()
        message.fromJson(str(data))
        user = message.getUser()
        if user in self.chats:
            chat = self.chats[user]
            chat.receiveMessage(message)
        else:
            self.refreshUsersList()
            addrs = self.userList[user]
            chat = Chat(self.username, user, addrs)
            self.chats[user] = chat
            chat.receiveMessage(message)

    def getUsers(self,host,port):
        client = Client(host,port)
        if(client.connect()):
            client.sendUsername(self.username)
            return client.receiveUserList()
        else:
            return {'Server error':None}

    def refreshUsersList(self):
        self.userList = self.getUsers(self.hostname,self.portnumber)
        users = list(self.userList)
        self.list.clear()
        self.list.addItems(users)

    def serverDisconnect(self,host,port):
        client = Client(host,port)
        if(client.connect()):
            client.sendUsername("REMOVE:"+self.username)

    def closeChat(self):
        self.serverDisconnect(self.hostname,self.portnumber)
        self.userserver.end()

    def __init__(self, username,hostname,portnumber):
        super(MainWindow, self).__init__()
        self.username = username
        self.hostname = hostname
        self.portnumber = portnumber

        self.userserver = UserServer()
        self.connect( self.userserver, QtCore.SIGNAL("update(QString)"), self.receivedMessage )
        self.userserver.start()
        
        self.chats = dict()
        title = "Users Connected"
        self.setWindowTitle(str(title))
        self.resize(300,400)

        self.layout = QtGui.QGridLayout(self)

        #users online listWidget 
        self.list = QtGui.QListWidget()
        self.userList = self.getUsers(self.hostname,self.portnumber)
        users = list(self.userList)
        self.list.addItems(users)
        self.layout.addWidget(self.list, 0, 0, 1, 3)
        self.connect(self.list,
             QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
             self.chatStarted)

        #selectbutton
        self.selectbutton = QtGui.QPushButton(self)
        self.selectbutton.setText("Chat")
        self.selectbutton.setMinimumWidth(20)
        self.selectbutton.setMinimumHeight(50)
        self.layout.addWidget(self.selectbutton, 1, 0)
        QtCore.QObject.connect(self.selectbutton, QtCore.SIGNAL("clicked()"), self.chatStarted)

        #refreshbutton
        self.refreshbutton = QtGui.QPushButton(self)
        self.refreshbutton.setText("Refresh")
        self.refreshbutton.setMinimumWidth(20)
        self.refreshbutton.setMinimumHeight(50)
        self.layout.addWidget(self.refreshbutton, 1, 1)
        QtCore.QObject.connect(self.refreshbutton, QtCore.SIGNAL("clicked()"), self.refreshUsersList)

        #logoutbutton
        self.logoutbutton = QtGui.QPushButton(self)
        self.logoutbutton.setText("Log out")
        self.logoutbutton.setMinimumWidth(5)
        self.logoutbutton.setMinimumHeight(50)
        self.layout.addWidget(self.logoutbutton, 1, 2)
        QtCore.QObject.connect(self.logoutbutton, QtCore.SIGNAL("clicked()"), self.closeChat)

        self.setLayout(self.layout)
        self.show()
