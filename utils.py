import socket, ssl, sys, errno
from PyQt4 import QtCore, QtGui
from datetime import datetime
import json


class Chat(QtGui.QDialog):

    def receiveMessage(self, message):
        self.chatLog.append(message)
        self.refreshChatMessages()

    def sendMessage(self, message):
        self.chatLog.append(message)
        self.refreshChatMessages()
        try:
            self.sslSocket.send(message.toJson())
        except ssl.SSLError as e:
            self.error = ErrorUI(str(e))
        except socket.error as e:
            errorcode = e[0]
            if errorcode == errno.EPIPE:
                self.error = ErrorUI("Could not send message")
                try:
                    self.sslSocket.close()
                except:
                    None

    def connect(self, ip):
        self.port = 5005
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sslSocket = ssl.wrap_socket(client, 
                        ssl_version=ssl.PROTOCOL_TLSv1)
        self.sslSocket.settimeout(3)
        try:
            self.sslSocket.connect((ip, self.port))
            return True
        except socket.error as e:
            errorcode = e[0]
            if errorcode == errno.ECONNREFUSED:
                self.error = ErrorUI("Could not connect to "+ self.contact)
            return False

    def clickedButton(self):
        text = self.messageText.text()
        message = Message(self.username, text)
        self.sendMessage(message)

    def refreshChatMessages(self):
        html = ""
        self.messageText.clear()
        for post in self.chatLog:
            if post.getUser() == self.username:
                html += '<div align="right">'
                html += post.getMessage()
                html += " ("
                html += post.getTime()
                html += ")"
            else:
                html += "<div>"
                html += "("
                html += post.getTime()
                html += ") "
                html += post.getMessage()
            html += "</div>"
        self.chatText.setHtml(html)

    def __init__(self, username, contact, ip):
        super(Chat, self).__init__()
        self.chatLog = []
        self.username = username
        self.contact = contact
        self.setWindowTitle(str(contact))
        self.resize(600, 400)
        self.layout = QtGui.QGridLayout(self)
        try:            
            if self.connect(ip):
                #Text
                self.scroll = QtGui.QScrollArea(self)
                self.scroll.setWidgetResizable(True)
                self.scrollAreaWidgetContents = QtGui.QWidget()
                self.scroll.setWidget(self.scrollAreaWidgetContents)
                self.chatText = QtGui.QTextBrowser(self.scrollAreaWidgetContents)
                self.layout.addWidget(self.scroll, 0, 0, 1, 2)
                self.layout.addWidget(self.chatText, 0, 0, 1, 2)

                #SendButton
                self.pushButton = QtGui.QPushButton(self)
                self.pushButton.setText("Send")
                self.pushButton.setMinimumWidth(50)
                self.pushButton.setMinimumHeight(45)
                QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.clickedButton)
                self.layout.addWidget(self.pushButton, 1, 1)

                #messageText
                self.messageText = QtGui.QLineEdit(self)
                self.layout.addWidget(self.messageText, 1, 0)

                self.setLayout(self.layout)
                self.show()

            else:
                self.accept()

        except Exception as e:
            print e;
class Message():

    def __init__(self, user="", message=""):
        self.time = str(datetime.now().time())[:-7]
        self.date = str(datetime.now().date())
        self.user = str(user)
        self.message = str(message)


    def getTime(self):
        return self.time

    def getDate(self):
        return self.date

    def getUser(self):
        return self.user

    def getMessage(self):
        return self.message

    def toJson(self):
        messageJson = {'time':self.time, 'date':self.date, 'user':self.user, 'message':self.message}
        return json.dumps(messageJson)

    def fromJson(self, messageJson):
        try:
            msgDict = json.loads(messageJson)
            self.time = msgDict['time']
            self.date = msgDict['date']
            self.user = msgDict['user']
            self.message = msgDict['message']
            return True
        except:
            False

class ErrorUI(QtGui.QDialog):

    def __init__(self, message):
        super(ErrorUI, self).__init__()
        self.setWindowTitle("Erro!")
        self.resize(500, 100)
        self.layout = QtGui.QGridLayout(self)
        errorLabel = QtGui.QLabel(message)
        self.layout.addWidget(errorLabel, 0, 0)
        self.setLayout(self.layout)
        self.show()