#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, select, sys, json


TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = raw_input("Start server at port: ")
BUFFER_SIZE = 1024


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", int(TCP_PORT)))
server.listen(5)

connections = []
connections.append(server)
users = dict()
socketIP = dict()


print "Server linstening on "+TCP_IP+":"+TCP_PORT

while 1:
	try:
		readable_sockets,writeable_sockets,error_sockets = select.select(connections,[],[])
	except:
		print "Closed"
		sys.exit(0)

	for s in readable_sockets:

		if s == server:
			connection, address = server.accept()
			socketIP[connection] = address[0]
			connections.append(connection)
			
		else:
			try:
				receivedData = s.recv(BUFFER_SIZE)
				if receivedData[0:7] == "REMOVE:":
					try:
						print "Removing: "+receivedData[7:]+"\nAddress: "+users[receivedData[7:]]
						del users[receivedData[7:]]
					except:
						None
				else:
					if not "GET" in receivedData:
						if(receivedData not in users):
							print receivedData + " connected"
						users[receivedData] = socketIP[s]
					s.send(json.dumps(users))
			except:
				print "Error receiving data"
			connections.remove(s)
			s.close()