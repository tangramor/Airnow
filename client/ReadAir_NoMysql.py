# -*- coding: utf-8 -*-   

import serial, time
from socketIO_client import SocketIO, LoggingNamespace

t = serial.Serial("com4", 2400)	# serial port and baudrate

with SocketIO('localhost', 8000, LoggingNamespace) as socketIO:	# connect socket.io server
	while True:
		str = t.readline()	# read from serial port
		
		socketIO.emit('airnow', str)	# raise event to socket.io server
		