'''
This is used to handle stdin and stdout input and output for the library
'''
import time
import sys
import threading
STDOUT_BUFFER = []


def print_stdout_buffer():
	'''Continously flushes the stdout buffer'''
	global STDOUT_BUFFER
	try:
		while 1:
			if STDOUT_BUFFER:
				out = STDOUT_BUFFER[0]
				STDOUT_BUFFER = STDOUT_BUFFER[1:]
				print >>sys.stdout, out
			time.sleep(.1)
	except Exception,e:
		print >>sys.stderr,"Error in printing to stdout:",e
		os._exit(1)

def stdout_print(string):
	'''Appends given string to the print/stdout buffer.
	To print a string:  io.stdout_print
	                             or
	                    standard_io.stdout_print'''
	STDOUT_BUFFER.append(string)

def start_io():
	'''Starts the input/output buffer flushing'''
	t = threading.Thread(target=print_stdout_buffer)
	t.start()

