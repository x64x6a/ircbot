#ircbot
======

##IRC Bot Python Library

This is an IRC library for Python that abstracts away the lower level details of interacting with an IRC server. You can use this library to automate IRC tasks or create a bot. This library uses SSL by default.

##Prerequisites

This library should work with with Python 2.7.6 or later.

##Installation

Run ``python setup.py install``.

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

Syntax to add a command involves creating your own function to run when that command is sent.
Your function needs to take 5 parameters:  func(self, sender, channel, cmd, params)

To add a command:
```python
def slap(self, sender, channel, cmd, params):
	message = 'slaps ' + (params.split(' ')[0] or sender) + " around a bit with a large trout"
	self.comm.perform_action(message, channel)
mybot.add_cmd('slap',slap)
```




