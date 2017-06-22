#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, json, sys


class Client():

	def __init__(self,host,port):
		self.server = None
		self.CLIENT_TCP_IP = socket.gethostbyname(socket.gethostname())
		self.SERVER_TCP_IP = host
		self.SERVER_TCP_PORT = int(port)
		self.BUFFER_SIZE = 1024


	def connect(self):
		global server
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.server.connect((self.SERVER_TCP_IP, self.SERVER_TCP_PORT))
			self.server.settimeout(3)
			return True
		except:
			return False
		
	def sendUsername(self, username):
		try:
			self.server.send(username)
		except:
			print "Could not send message, disconnecting"

	def receiveUserList(self):
		userList = dict()
		try:
			data = self.server.recv(self.BUFFER_SIZE)
			self.server.close()
			try:
				userList = dict(json.loads(data))
			except:
				None
		except socket.timeout:
			None
		return userList