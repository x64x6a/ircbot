'''
This handles socket communcation for comm.py
'''
import socket
import ssl
import threading
import os
import sys
import time

######################################################################
#                                                                    #
#          Socket Handling                                           #
#                                                                    #
######################################################################
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
RECV_BUFFER = []
SEND_BUFFER = []

def recv_data():
	'''Receives data'''
	return IRC.recv(4096)

def recv_buffer():
	'''Continously gets the next input, and adds into buffer queue'''
	global RECV_BUFFER
	try:
		while 1:
			data = recv_data()
			data = data.split('\n')
			for buff in data:
				if buff:
					RECV_BUFFER.append(buff)
			time.sleep(1)
	except Exception,e:
		print >>sys.stderr,"Exception in receive socket:",e
		os._exit(1)

def send_buffer():
	'''Continously attempts to send the next output from a buffer'''
	global SEND_BUFFER
	try:
		while 1:
			if SEND_BUFFER:
				message = SEND_BUFFER[0]
				SEND_BUFFER = SEND_BUFFER[1:]
				IRC.send(message)
			time.sleep(1)
	except Exception,e:
		print >>sys.stderr,"Exception in send socket:",e
		os._exit(1)

def getNext():
	'''Gets the next data in the buffer'''
	global RECV_BUFFER
	if RECV_BUFFER:
		buffer = RECV_BUFFER[0]
		RECV_BUFFER = RECV_BUFFER[1:]
		return buffer
	else:
		return ''

def send_data(command, private=0):
	'''Simple function to send data through the socket'''
	if not private:
		#print "<",command,'\n\n'
		io.stdout_print("<"+command+'\n\n')
	SEND_BUFFER.append(command + '\n')

def conn((server, port), sslOn=True):
	'''Open a connection with the server.  SSL is on by default.'''
	if sslOn:
		global IRC
		IRC = ssl.wrap_socket(IRC)
	# connect to server
	IRC.connect((server, port))
	
	# spawn thread to continously get data
	t = threading.Thread(target=recv_buffer)
	t.start()
	
	# spawn thread to continously send data
	t = threading.Thread(target=send_buffer)
	t.start()
	
	global io
	import standard_io as io
	io.start_io()
	return io


def disconnect():
	'''Disconnects the socket'''
	IRC.shutdown(socket.SHUT_WR)
	IRC.close()
