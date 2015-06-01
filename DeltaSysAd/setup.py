#!/usr/bin/env python
import MySQLdb
import sys

try:
	conn = MySQLdb.connect('localhost', 'root', '')
	cursor = conn.cursor()
	cursor.execute("CREATE DATABASE Delta_SysAd_Task_2")
	cursor.execute("USE Delta_SysAd_Task_2")
	cursor.execute("""
		CREATE TABLE time_keeper (
			time_col    TIMESTAMP
		)
	""")
	cursor.close()
	conn.close()

except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)
