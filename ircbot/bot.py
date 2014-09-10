'''
This can be used primarily to start and setup an IRC bot.  It can be used as is, but the
bot will not have much functionality.  It will simply join a server of your choice with
the given user credentials.  You must be registered on the IRC server, so the password 
field is required.  If you want to add commands that your IRC bot will read, you can add
them the the bot.Bot.add_cmd() function.  You may also want to take a look at comm.py

By default, commands are read in from channel messages.  For example, someone saying 
'!slap Nick' in a channel that the bot is in would proc the 'slap' command, and the bot
would respond by slapping Nick around a bit with a large trout.

Things to note:
	 - This bot was setup specifically for Freenode IRC
	 - A lot of threads are going to spawn :)
	 - Your nick must be registered to use

To use add_cmd(), your function should take parameters like so:
	func(self, sender, channel, cmd, params)

Example:
	
	def slap(self, sender, channel, cmd, params):
		message = 'slaps ' + (params.split(' ')[0] or sender) + " around a bit with a large trout"
		self.comm.perform_action(message, channel)
	
	bot = ircbot.bot('chat.freenode.net', 6665, 'Nick', 'Nick', 'password1234', 'Nicolas', 'Host', 'chat.freenode.net')
	bot.add_cmd('slap', slap)
	bot.conn()
	bot.join('#channel')
	
	
'''
import threading
import re
import time

class Bot():
	def __init__(self, server, port, nickname, username, password, realname, hostname, servername, logs=False, cmdIdentifier='!'):
		'''initialize:  server, port, nickname, username, password, realname, hostname, servername
		Password can be None.  Set the logs flag to true to save logs.'''
		self.server = server
		self.port = port
		self.nickname = nickname
		self.username = username
		self.password = password
		self.realname = realname
		self.hostname = hostname
		self.servername = servername
		
		self.cmdIdentifier = cmdIdentifier  # default identifier is '!'
		self.commands = {}
		import comm
		self.comm = comm #__import__('comm')
		self.channel_list = []
		self.chanserv = 'ChanServ'  # for accessing channel permissions
		self.accessLists = {}  # for obtaining channel access lists
		self.logs = logs
		self.log_dir = self.nickname + '_logs'
		self.logfile = self.log_dir + '/ircbotlog.txt'
		self.canJoin = False
		self.lastUpdate = 0
		
		# if logs is turn on, confirm directory exists
		if self.logs and not os.path.exists(self.log_dir):
			os.mkdir(self.log_dir)
		
	
	def conn(self):
		'''Connect to IRC server, logs in, and starts the message handler'''
		self.comm.conn((self.server, self.port))
		self.comm.login(self.nickname, self.username, self.password, self.realname, self.hostname, self.servername)
		
		# start handler
		t = threading.Thread(target=self.handler)
		t.start()
	
	def join(self, channel):
		'''Join the given channel'''
		# infinite loop until self.conJoin flag is set
		while not self.canJoin:
			time.sleep(5)
		self.comm.join(channel)
	
	def recv(self):
		'''Recommended to not use this function directly.  The function, handler(), will process input/output.'''
		self.comm.recv()
	
	def disconnect(self, message='Goodbye cruel world!'):
		'''Disconnects the bot from IRC with message'''
		self.comm.disconnect(message)
	
	def handleCmd(self, buffer):
		'''Handles commands.  Handler() is meant to spawn a new thread when calling handleCmd() to increase speed.'''
		# syntax is:
		#      :user!user@ip PRIVMSG #channel :!command <optional params>
		bufflist = buffer.split(' ')
		cmd = bufflist[3][2:]  # get cmd ASAP
		
		if cmd not in self.commands:
			return
		
		sender = bufflist[0][:bufflist[0].find('!')][1:]  # get sender
		channel = bufflist[2]  # get channel
		
		# get params if there are any
		params = ''
		if len(bufflist) > 4:
			params = ' '.join(bufflist[4:])
		
		func = self.commands[cmd]  # get function
		func(self, sender, channel, cmd, params) # call function
	# end handleCmd
	
	def handleAccessList(self, messageList):
		''' Attempts to handle notice's from chanserve contain the users' flags.  May fail.
		If it doesn't... it will add the access list to self.flag_dict[channel]'''
		print "Updating Flags....\n\n"
		messages = '\n'.join(messageList)
		pattern = r"\d+\s+[A-Za-z0-9_]+\s+\+[A-Za-z]+"
		found = re.findall(pattern, messages)
		
		if not found:
			return 
		
		flag_dict = {}
		for set in found:
			set = set.replace('\t',' ')
			while '  ' in set:
				set = set[:set.find('  ')] + set[set.find('  ')+1:]
			set = set.split(' ')
			
			user = set[1]
			flags = set[2][1:]
			
			for flag in flags:
				if flag not in flag_dict:
					flag_dict[flag] = [user]
				else:
					flag_dict[flag].append(user)
		print flag_dict
		# last appended message should contain the channel
		n = messageList[-1].find('\x02#')
		if n == -1: return
		channel = messageList[-1][messageList[-1].find('\x02#')+1:]
		n = channel.find('\x02')
		if n == -1: return
		channel = channel[:n]
		
		# set the channels flags
		self.accessLists[channel] = flag_dict
	# end handleAccessList
	
	def handler(self):
		'''Handles input and sends responses for the bot'''
		isCmd = re.compile(r'\S+ PRIVMSG #\S+ :!.+', re.IGNORECASE)
		wasKicked = re.compile(r'\S+ KICK #\S+ ' + self.nickname + r' :.*', re.IGNORECASE)
		isChanServNotice = re.compile(r':' + self.chanserv + r'!\S+ NOTICE ' + self.nickname + r' :.+', re.IGNORECASE)
		isBotJoin = re.compile(r':' + self.nickname + r'!\S+ JOIN #\S+', re.IGNORECASE)
		cs_noticeList = []  # list of notices from chanserv
		
		# set f if loggin is on
		f = False
		if self.logs:
			f = open(self.logfile,'a+')
		
		while True:
			# get next input
			buffer = self.comm.recv()
			if buffer:
				print buffer
			else:
				continue
			
			# disallow joins until identified
			if not self.canJoin and "You are now identified for \x02" + self.nickname + "\x02" in buffer:
				self.canJoin = True
			
			if f:  f.write(buffer + '\n')
			
			
			
			# check if ping, to respond with pong
			if buffer[:5] == 'PING ':
				sender = buffer.split(' ')[1]
				self.comm.pong(sender)
				continue
			# check if command message from channel
			if isCmd.match(buffer):
				t = threading.Thread(target=self.handleCmd, args=(buffer,))
				t.start()
				continue
			# check if joining a channel
			if isBotJoin.match(buffer):
				channel = buffer.split(' ')[2]
				if channel in self.channel_list:
					continue
				self.channel_list.append(channel)
				self.updateAccess(channel)
				continue
			# check if was kicked, rejoin if so
			if wasKicked.match(buffer):
				channel = buffer.split(' ')[2]
				if channel in self.channel_list:
					self.channel_list.remove(channel)
				self.comm.join(channel)
				continue
			# catch chanserv notices
			if isChanServNotice.match(buffer):
				# just hope no other chanserv notices distrupt this...
				messageList = buffer.split(' ')[3:]
				message = ' '.join(messageList)[1:]
				
				if messageList[0][1:].lower() == 'entry':
					cs_noticeList = []
				cs_noticeList.append(message)
				print "HEREREREE:>>>  ",messageList, "\n<<<<<<<<<<<<<\n\n"
				# last appended message should contain the channel
				if messageList[0][1:].lower() == 'end':
					t = threading.Thread(target=self.handleAccessList, args=(cs_noticeList,))
					t.start()
				continue
	# end handler
	
	def updateAccess(self, channel):
		'''This function is used to update the bot's channel access lists for a given channel'''
		thisUpdate = int(time.time())
		
		# wait at least 10 minutes before requesting another update
		if (thisUpdate - self.lastUpdate) / 60 < 10:
			return
		
		message = "flags " + channel
		self.comm.messageUser(message, self.chanserv)
	
	def add_cmd(self, command, function):
		'''This adds the given command and runs function when a users says !command
The function should take parameters like:
		func(self, sender, channel, cmd, params)'''
		self.commands[command] = function










