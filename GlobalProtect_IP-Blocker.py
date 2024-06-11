'''Python SysllogServer which creates User in Paloalto-FW for blocking source-IP'''

LOG_FILE = "syslogfile.txt"
HOST, PORT = "0.0.0.0", 514
BlockingDuration = 14400 # 4 hours Blocking 

import logging
import socketserver
from panos import firewall
from dotenv import dotenv_values

# Fielddescriptions get when CSV-export from Global-Protect-Log 
LoggingData="Domain,Receive Time,Serial #,Type,Threat/Content Type,Config Version,Generate Time,Virtual System,Event ID,Stage,Authentication Method,Tunnel Type,Source User,Source Region,Machine Name,Public IP,Public IPv6,Private IP,Private IPv6,Host ID,Serial Number,Client Version,Client OS,Client OS Version,Repeat Count,Reason,Error,Description,Status,Location,Login Duration,Connect Method,Error Code,Portal,Sequence Number,Action Flags,High Res Timestamp,Selection Type,Response Time,Priority,Attempted Gateways,Gateway,DG Hierarchy Level 1,DG Hierarchy Level 2,DG Hierarchy Level 3,DG Hierarchy Level 4,Virtual System Name,Device Name,Virtual System ID,cluster_name,project_name"
index_IP=0
index_username=0
badusers = []

def prep_data(): # Used to find Index Position from Username and PublicIP Field in syslog
	global LoggingData,index_IP,index_username,badusers
	fieldlist=LoggingData.split(',')
	index_IP=fieldlist.index('Public IP')
	index_username=fieldlist.index('Source User')
	with open('BadUsernames.txt', 'r') as f:
		file = f.read()
	badusers = [name.lower().strip() for name in file.split("\n") ] #remove whitespace and lower badusers

def request_block(IP):
	# TAG IP address with "BadGPIP" for 1 hour
	fw.userid.register(f'{IP}',"BadGPIP",timeout=BlockingDuration)

def data_handling(data):
	global index_IP, index_username
	data_list=data.split(',')
	user=data_list[index_username]
	IP=data_list[index_IP]
	print (f"User: {user} tryed to login from {IP}")
	if user.lower() in badusers:
		request_block(IP)
		print(f"IP Address {IP} was tagged as BadGPIP")
	return
	
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

class SyslogUDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		print( "%s : " % self.client_address[0], str(data))
		data_handling(data)
		logging.info(str(data))

if __name__ == "__main__":
	prep_data()
	envparameter=dotenv_values('.env')
	fw = firewall.Firewall(envparameter["pa_IP"], api_username=envparameter["pa_user"], api_password=envparameter["pa_passwd"]) # connect to Firewall with crets from .env file
	print ('started syslogserver on UDP-Port 514, events will printed here\n++++++++++++++\n')
	try:
		server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")