'''
	Example of implementation of ircbot library
'''
import ircbot.bot as bot

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
	# *** EDIT PARAMETERS ***    # SSL is on by default... make sure your using an ssl enabled port
	mybot = bot.Bot('chat.freenode.net', 6697, 'IamBot10110', 'IamBot10110', 'PASSWORD1234', 'Name', 'Host', 'chat.freenode.net')
	
	# add commands
	mybot.add_cmd('slap',slap)
	mybot.add_cmd('op', op)
	mybot.add_cmd('deop', deop)
	
	# connect
	mybot.conn()
	
	# join channel 
	mybot.join('#channel')
	
	# speak in channel
	mybot.comm.messageChannel('This is a Test!','#channel')

if __name__ == "__main__":
	main()






