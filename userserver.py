import socket, select, sys, ssl, os.path
from PyQt4 import QtCore
from utils import Message
from OpenSSL import crypto

class UserServer(QtCore.QThread):

	def __init__(self):
		QtCore.QThread.__init__(self)
		self.IP = socket.gethostbyname(socket.gethostname())
		self.TCP_PORT = 5005
		self.BUFFER_SIZE = 1024
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.running=False
		self.serversocket.bind((self.IP, self.TCP_PORT))
		self.serversocket.listen(5)

		self.generate_certificate()

		self.connections = []
		self.connections.append(self.serversocket)


	def generate_certificate(self):
		certificate_file_name = "mycert.pem"
		key_file_name = "mykey.key"
		
		if os.path.isfile(certificate_file_name) and os.path.isfile(key_file_name):
			return
		else:
			mykey = crypto.PKey()
			mykey.generate_key(crypto.TYPE_RSA, 1024)

			mycertificate = crypto.X509()

			mycertificate.get_subject().C = "BR"
			mycertificate.get_subject().ST = "Rio de Janeiro"
			mycertificate.get_subject().L = "Rio de Janeiro"
			mycertificate.get_subject().O = "UFRJ"
			mycertificate.get_subject().OU = "UFRJ"
			mycertificate.get_subject().CN = self.IP

			mycertificate.gmtime_adj_notBefore(0)
			mycertificate.gmtime_adj_notAfter(365*24*60*60)

			mycertificate.set_issuer(mycertificate.get_subject())
			mycertificate.set_pubkey(mykey)
			mycertificate.sign(mykey, 'sha1')

			mycertificate_file = open(certificate_file_name, "wt")
			mycertificate_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, mycertificate))
			mycertificate_file.close()

			key_file = open(key_file_name, "wt")
			key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, mykey))
			key_file.close()


	def run(self):
		self.running = True
		while self.running:
			try:
				readable_sockets,writeable_sockets,error_sockets = select.select(self.connections,[],[])
			except:
				break
			for s in readable_sockets:
				if s == self.serversocket:
					connection, address = self.serversocket.accept()
					sslconnection = ssl.wrap_socket(connection,
								server_side=True,
								certfile="mycert.pem",
								keyfile="mykey.key",
								ssl_version=ssl.PROTOCOL_TLSv1)
					self.connections.append(sslconnection)
				else:
					try:
						data = s.recv(self.BUFFER_SIZE)
						if data == "":
							s.close()
							connections.remove(s)
						self.emit(QtCore.SIGNAL('update(QString)'), data)
					except:
						break
					
					
			
	def end(self):
		self.running = False
		for conn in self.connections:
			conn.close()
		self.serversocket.close()
		sys.exit(0)