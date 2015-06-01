#!/usr/bin/env python

'''
Author: 		Parth Thakkar
Description:	This script was written as a part of Delta Sys Ad
				inductions.

This was serious fun.
'''

import os
import stat
import MySQLdb
import sys
import getopt
import datetime
import subprocess

usage_info = '''DB_Scriptception.py usage:
DB_Scriptception.py -m <host> -u <username> -p <password> <location> 

Warning:	Invoke this script only via python2 interpreter
Arguments:
location:	Location as to where the scripts must be created
			Default: Current working directory

Options:
-h          Display this help
-m          Name of the machine that hosts MySQL server.
			Default: 'localhost'
-u          Username of the database.
			Default: 'root'
-p          Password of the user specified
			Default: '' (empty)
'''

# color codes taken from stack overflow. :P
# Only for pretty-printing.
class FancyOutput:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def make_exec(file_name):
	try:
		mode = os.stat(file_name)
		os.chmod(file_name, mode.st_mode | stat.S_IEXEC)	# make the script executable by the user alone.
	except:
		print FancyOutput.WARNING + "Failed to make " + FancyOutput.UNDERLINE + \
			os.path.basename(file_name) + FancyOutput.ENDC + FancyOutput.WARNING + \
			" executable." + FancyOutput.ENDC
		print "It has, however, been created.\n"
		raise


def writeSetupScript(host, username, password, location):
	try:
		code = '''\
#!/usr/bin/env python
import MySQLdb
import sys

try:
	conn = MySQLdb.connect('{0}', '{1}', '{2}')
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
'''
	
		code = code.format(host, username, password)

		file_name = location
		location += "/setup.py" if location[-1] != "/" else "setup.py"

		out = open(location, "w")
		out.write(code)
		out.close()

		print FancyOutput.OKGREEN + "1. Successfully created the setup.py file (" + FancyOutput.UNDERLINE + location + ")" + FancyOutput.ENDC
		make_exec(location)

	except:
		print FancyOutput.FAIL + "1. Failed to create the setup.py file" + FancyOutput.ENDC
		raise

def writeUpdateScript(host, username, password, location):
	try :
		code = '''\
#!/usr/bin/env python
import MySQLdb
import sys

try:
	conn = MySQLdb.connect('{0}', '{1}', '{2}')
	cursor = conn.cursor()
	cursor.execute("USE Delta_SysAd_Task_2")
	cursor.execute("""
		INSERT INTO time_keeper VALUES ('{3}')
	""")
	cursor.close()
	conn.commit()
	conn.close()

except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)
'''
		
		code = code.format(host, username, password, datetime.datetime.now())

		file_name = location
		location += "/update.py" if location[-1] != "/" else "update.py"

		out = open(location, "w")
		out.write(code)
		out.close()

		print FancyOutput.OKGREEN + "2. Successfully created the update.py file (" + FancyOutput.UNDERLINE + location + ")" + FancyOutput.ENDC
		make_exec(location)

	except:
		print FancyOutput.FAIL + "2. Failed to create the update.py file" + FancyOutput.ENDC
		raise

def setupCron(location):
	try:
		location_f = "/update.py" if location[-1] != "/" else "update.py"

		cmd = subprocess.Popen("crontab -l", shell=True, stdout=subprocess.PIPE).stdout.read()
		cmd += "*/10 * * * * /usr/bin/env python " + location_f + "\n"
		
		# temporary file. Will be deleted automatically.
		tmp = open("/tmp/temp_cron.impossible", 'w')
		tmp.write(cmd)
		tmp.close()

		subprocess.Popen("crontab /tmp/temp_cron.impossible", shell=True)

		print FancyOutput.OKGREEN + "3. Successfully set up the cron job." + FancyOutput.ENDC

	except:
		print FancyOutput.WARNING + "Error writing the cron job. The scripts have been made though." + FancyOutput.ENDC
		# don't raise. We've warned the user.

def main(argv):
	host = 'localhost'
	username = 'root'
	password = ''
	location = os.getcwd()

	try:
		opts, remainder = getopt.getopt(argv,"hm:u:p:")
	except getopt.GetoptError:
		print usage_info
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print usage_info
			sys.exit()
		if opt == '-m':
			host = arg
		if opt == '-u':
			username = arg
		if opt == '-p':
			password = arg

	if len(remainder) > 1:
		print FancyOutput.FAIL + "Enter a valid location. Use 'DB_Scriptception.py -h' for help." + FancyOutput.ENDC
		sys.exit(2)

	if len(remainder) == 1:
		location = remainder[0]

	writeSetupScript(host, username, password, location)
	writeUpdateScript(host, username, password, location)
	setupCron(location)

	print "Done."
	
if __name__ == "__main__":
	main(sys.argv[1:])
