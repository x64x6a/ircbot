#ircbot
======

##IRC Bot Python Library

This library can be used to setup a bot to automate tasks on an IRC server.  It was primarily designed to join a channel(s) and accept commands via the channel's messages.
This library, by default, uses SSL.

##Installation

Known to work with Python 2.7.6 or later.

Run ``python setup.py install``

##Example

Basic implementation:
```python
from ircbot import bot

# initialize
mybot = bot.Bot('chat.freenode.net', 6697, 'IamBot10110', 'IamBot10110', 'PASSWORD1234', 'Name', 'Host', 'chat.freenode.net', sslOn=True)

# connect
mybot.conn()

# join channel 
mybot.join('#channel')

# speak in channel
mybot.comm.messageChannel('This is a Test!','#channel')
```

Syntax to add a command involves creation your own function to run when that command is sent.
Your function needs to take 5 parameters:  func(self, sender, channel, cmd, params)

To add a command:
```python
def slap(self, sender, channel, cmd, params):
	message = 'slaps ' + (params.split(' ')[0] or sender) + " around a bit with a large trout"
	self.comm.perform_action(message, channel)
mybot.add_cmd('slap',slap)
```




