'''
	Example of implementation of ircbot library
'''
import ircbot.bot as b
import time

# func(self, sender, channel, cmd, params) # call function
def slap(self, sender, channel, cmd, params):
	message = 'slaps ' + (params.split(' ')[0] or sender) + " around a bit with a large trout"
	self.comm.perform_action(message, channel)

def op(self, sender, channel, cmd, params):
	access_list = self.accessLists[channel]
	if sender in access_list['O']:
		# params is empty string by default
		message = 'flags ' + channel + ' ' + (params.split(' ')[0] or sender) + ' -Oo'
		self.comm.messageUser(message, self.chanserv)

def deop(self, sender, channel, cmd, params):
	access_list = self.accessLists[channel]
	if sender in access_list['O']:
		# params is empty string by default
		message = 'flags ' + channel + ' ' + (params.split(' ')[0] or sender) + ' -Oo'
		self.comm.messageUser(message, self.chanserv)

def main():
	# *** EDIT PARAMETERS ***
	bot = b.Bot('chat.freenode.net', 6665, 'IamBot10110', 'IamBot10110', 'PASSWORD1234', 'Name', 'Host', 'chat.freenode.net')
	
	# add commands
	bot.add_cmd('slap',slap)
	bot.add_cmd('op', op)
	
	# connect
	bot.conn()
	
	# join channel 
	bot.join('#unonullify')
	
	# speak in channel
	bot.comm.messageChannel('This is a Test!','#unonullify')

if __name__ == "__main__":
	main()






