'''
This handles socket communcation for irccomm
'''
import socket
import threading

######################################################################
#                                                                    #
#          Socket Handling                                           #
#                                                                    #
######################################################################
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BUFFER = []

def recv_data():
	'''Receives data'''
	return IRC.recv(4096)

def recv_buffer():
	'''Continously gets the next input, and adds into buffer queue'''
	try:
		while 1:
			data = recv_data()
			data = data.split('\n')
			for buff in data:
				if buff:
					BUFFER.append(buff)
	except:
		return

def getNext():
	'''Gets the next data in the buffer'''
	global BUFFER
	if BUFFER:
		buffer = BUFFER[0]
		BUFFER = BUFFER[1:]
		return buffer
	else:
		return ''

def send_data(command, private=0):
	'''Simple function to send data through the socket'''
	print ">  Sending:  " + command + "\n"
	IRC.send(command + '\n')

def conn((server, port)):
	'''Open a connection with the server'''
	# connect to server
	IRC.connect((server, port))
	
	# spawn thread to continously get data
	t = threading.Thread(target=recv_buffer)
	t.start()

def disconnect():
	'''Disconnects the socket'''
	IRC.shutdown(socket.SHUT_WR)
	IRC.close()

