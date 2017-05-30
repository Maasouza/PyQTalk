from PyQt4 import QtCore, QtGui
import sys
from mainwindow import MainWindow
#from error import Error

class Login(QtGui.QDialog):

    def __init__(self):
        super(Login, self).__init__()
        title = "Login"
        self.setWindowTitle(str(title))
        
        self.layout = QtGui.QGridLayout(self)

        #name input
        self.nameInput = QtGui.QLineEdit('', self)
        self.nameInput.setStyleSheet("font: 20pt")
        self.nameInput.setFixedHeight(30)
        self.layout.addWidget(self.nameInput, 1,0)
        userLabel = QtGui.QLabel('USER:')
        self.layout.addWidget(userLabel, 0, 0)


        #ip input
        self.ipInput = QtGui.QLineEdit('', self)
        self.ipInput.setStyleSheet("font: 20pt")
        self.ipInput.setFixedHeight(30)
        self.layout.addWidget(self.ipInput, 3, 0)
        ipLabel = QtGui.QLabel('HOST:')
        self.layout.addWidget(ipLabel, 2, 0)

        self.portInput = QtGui.QLineEdit('', self)
        self.portInput.setStyleSheet("font: 20pt")
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

        #Crypto group
        """CIPHER STRINGS  link:https://www.mkssoftware.com/docs/man1/openssl_ciphers.1.asp
            The following is a list of all permitted cipher strings and their meanings:

            DEFAULT 
            the default cipher list. This is determined at compile time and is normally ALL:!ADH:RC4+RSA:+SSLv2:@STRENGTH. This must be the first cipher string specified.

            ALL 
            all ciphers suites except the eNULL ciphers which musti be explicitly enabled.

            HIGH 
            "high" encryption cipher suites. This currently means those with key lengths larger than 128 bits.

            MEDIUM 
            "medium" encryption cipher suites currently those using 128 bit encryption.

            LOW 
            "low" encryption cipher suites currently those using 64 or 56 bit encryption algorithms but excluding export cipher suites."""

        self.cryptoBoxes = []

        #list -> terminal >openssl cipher -V
        ciphers = ["AES256-SHA", "AES128-SHA", "RC4-SHA"]

        self.cryptoGroup = QtGui.QGroupBox("Ciphers", self)
        self.cryptoGroup.setStyleSheet("font: 13pt")
        self.cryptoGroupLayout = QtGui.QGridLayout()
        allBox = QtGui.QCheckBox("ALL")
        allBox.setChecked(True)
        self.cryptoBoxes.append(allBox)
        self.cryptoGroupLayout.addWidget(allBox, 0, 0)
        highBox = QtGui.QCheckBox("HIGH")
        highBox.setToolTip("Encryption cipher suites.\nThis currently means those with key lengths larger than 128 bits.")
        self.cryptoBoxes.append(highBox)
        self.cryptoGroupLayout.addWidget(highBox, 1, 0)
        mediumBox = QtGui.QCheckBox("MEDIUM")
        mediumBox.setToolTip("Encryption cipher suites currently those using 128 bit encryption.")
        self.cryptoBoxes.append(mediumBox)
        self.cryptoGroupLayout.addWidget(mediumBox, 2, 0)
        lowBox = QtGui.QCheckBox("LOW")
        lowBox.setToolTip("Encryption cipher suites currently those using 64 or 56 bit encryption algorithms\nBut excluding export cipher suites")
        self.cryptoBoxes.append(lowBox)
        self.cryptoGroupLayout.addWidget(lowBox, 3, 0)
        for cipher in ciphers:
            cipherBox = QtGui.QCheckBox(cipher)
            self.cryptoBoxes.append(cipherBox)
            self.cryptoGroupLayout.addWidget(cipherBox, ciphers.index(cipher), 1)

        self.cryptoGroup.setLayout(self.cryptoGroupLayout)
        self.layout.addWidget(self.cryptoGroup, 6, 0, 1, 2)

        self.setLayout(self.layout)

    def doLogin(self):
        username = str(self.nameInput.text())
        hostname = str(self.ipInput.text())
        portnumber = str(self.portInput.text())

        ciphersList = ""
        for checkBox in self.cryptoBoxes:
            if checkBox.isChecked():
                name = str(checkBox.text())
                ciphersList+=(name+":")

        #remove ":" from end         
        ciphersList = ciphersList.strip(':')

        #dont allow no user or REMOVE(command to disconnect) and empty cipher 
        if username != "" and username[0:7] != "REMOVE:" and ciphersList:
            self.userMainWindow = MainWindow(username, ciphersList,hostname,portnumber)
            self.accept()
        else:
            self.error = Error("Username and cipher must be set.")

app = QtGui.QApplication(sys.argv)
usernameWindow = Login()
usernameWindow.show()

sys.exit(app.exec_())