from irc import bot
import os,threading,time

servers = [
	bot.ServerSpec("barjavel.freenode.net", 6667),
]
overlord = bot.SingleServerIRCBot(servers, "somebotname9797","boop")

def start():
	'''Function to run and start server'''
	return overlord.start()

def commands():
	'''Function to run all commands while the server is running'''
	# join a channel
	print overlord.connection.join("#test_channel")
	
	# done
	print "Finished commands"

if __name__ == '__main__':
	# start server on another thread, so we can send commands such as JOIN
	start = threading.Thread(target=start)
	start.start()
	
	# ghetto way to check if we are connected
	while 1:
		try:
			commands()
			break
		except:
			# catch error thrown when server is not connected
			time.sleep(3)
			continue
	
	# for catching ctrl+c to unsafely kill entire program
	while 1:
		try:
			time.sleep(1000)
		except:
			os._exit(1)
