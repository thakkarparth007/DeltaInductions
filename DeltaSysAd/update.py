#!/usr/bin/env python
import MySQLdb
import sys

try:
	conn = MySQLdb.connect('localhost', 'root', '')
	cursor = conn.cursor()
	cursor.execute("USE Delta_SysAd_Task_2")
	cursor.execute("""
		INSERT INTO time_keeper VALUES ('2015-06-01 19:08:16.437971')
	""")
	cursor.close()
	conn.commit()
	conn.close()

except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)
