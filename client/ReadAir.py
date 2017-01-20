# -*- coding: utf-8 -*-   

import serial, time, MySQLdb, re
from socketIO_client import SocketIO, LoggingNamespace

# open a mysql connection
conn=MySQLdb.connect(host="localhost",user="airnow",passwd="password",db="airnow",charset="utf8")

''' SQL to create table: 
CREATE TABLE IF NOT EXISTS `air_logs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pm25` float NOT NULL,
  `aqi` int(11) NOT NULL,
  `time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

sql = "INSERT INTO air_logs(`pm25`,`aqi`,`time`) VALUES(%s,%s,NOW())"

t = serial.Serial("com4", 2400)	# serial port and baudrate
i = 0
with SocketIO('localhost', 8000, LoggingNamespace) as socketIO:	# connect socket.io server
	while True:
		i = i + 1
		str = t.readline()	# read from serial port
		
		socketIO.emit('airnow', str)	# raise event to socket.io server
		
		# record data to mysql
		if i == 30:	# about 30 seconds insert 1 record to database
			i = 0 # reset counter
			cursor = conn.cursor()
			vals = re.split('[:; ]', str)	# the str gotten from serial port is: "PM2.5:11.53; AQI:15;"
			param = (vals[1], vals[4])	# put PM2.5 value and AQI value to param
			n = cursor.execute(sql, param)	# execute the sql query
			cursor.execute("commit")
			#print str	#Debug
			cursor.close()

# close mysql connection
conn.close()