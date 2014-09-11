'''
This is used to communicate to the socket via IRC protocol.
Recommended to use the bot.Bot class to create a bot instead of this.
HOWEVER, this is recommended to use this to add commands to your bot.

Example of use:
	SERVER, PORT = "chat.freenode.net", 6697
	
	# connect
	comm.conn((SERVER, PORT))
	
	# login as user Nick 
	comm.login("Nick", username="Nick", password="Password1234", realname='Nicolas',hostname='Host',servername=SERVER )
	
	# join channel
	comm.join("#channel")
	
	# message a user
	comm.messageUser("Hello!", "User")
	
	# disconnect from irc
	comm.disconnect("Off to do the dishes...")
	
'''
import ircsocket as sock


######################################################################
#                                                                    #
#          IRC (Send) Protocol                                       #
#                                                                    #
######################################################################

###################################
#         Basic Commands          #
###################################

def conn((server, port), sslOn=True):
	'''Connect to irc server at port.  SSL is on by default.'''
	sock.conn((server, port), sslOn)

def login(nickname, username, password, realname, hostname, servername):
	'''Send login data'''
	sock.send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
	# send optional password
	if password:
		sock.send_data("PASS %s" % password, 1)
	sock.send_data("NICK " + nickname)

def join(channel):
	'''Join a channel'''
	sock.send_data("JOIN %s" % channel)

def pong(sender):
	'''For a reply to ping, reply with pong as per RFC 1459'''
	sock.send_data("PONG :%s" % sender)

def disconnect(message):
	'''Disconnect with given message'''
	sock.send_data('QUIT :%s' % message)
	sock.disconnect()


###################################
#      Extra Utility Commands     #
###################################

def messageUser(message, user):
	'''Message a given user'''
	sock.send_data('PRIVMSG %s :%s' % (user, message))

def messageChannel(message, channel):
	'''Message a given channel'''
	sock.send_data('PRIVMSG %s :%s' %  (channel, message))

def cmessageUser(message, user, channel):
	'''Sends a private message to a user on the channel. Both 
users must be in that channel. Bypasses flood protection limits'''
	sock.send_data('CPRIVMSG %s %s :s' % (user, channel, message))

def noticeUser(message, user):
	'''Sends a notice to a user.  Notices are very similar to private messages.'''
	sock.send_data('NOTICE %s :%s' % (user, message))

def cnoticeUser(message, channel, user):
	'''Sends a channel notice to user.  Bypasses flood protection limits.'''
	sock.send_data('CNOTICE %s %s :%s' % (user, channel, message))

def change_topic(topic, channel):
	'''Change topic for channel'''
	sock.send_data("TOPIC %s :" % (channel, topic))

def kick_user(user, channel, reason='GTFO'):
	'''Kick a user from channel with a reason'''
	sock.send_data("KICK %s %s :%s" % (channel, user, reason))

def invite(user, channel):
	'''Invites a user to the channel'''
	sock.send_data("INVITE %s %s" % (user, channel))

def perform_action(action, channel):
	'''Performs the given action, commonly refered to as the /me command.
Channel can be a channel or a user'''
	message = "\x01ACTION " + action + "\x01"
	messageChannel(message, channel)


######################################################################
#                                                                    #
#          IRC (Recv) Protocol                                       #
#                                                                    #
######################################################################

def recv():
	'''Get the next data from the IRC server'''
	buff = sock.getNext().replace('\r','').replace('\n','')
	return buff

