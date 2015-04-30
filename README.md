#ircbot

This Python library is designed to communicate with an IRC server using the IRC protocol.  This library may be used to automate IRC problems or other tasks, such as creating a bot.  The library connects using SSL by default.

It should be noted that this project was created to learn more about IRC and the IRC protocol, so it may not be entirely perfect in nature.  However, it may be useful for understanding the IRC protocol or in creating an IRC bot that runs channel commands.

Other Python IRC options :
* [irc](https://pypi.python.org/pypi/irchttps://pypi.python.org/pypi/irc)
* [twisted](https://pypi.python.org/pypi/Twisted)

A simple example of using irc python library can be found [here](irc_example.py).  It can be installed with `pip install irc`.

##Prerequisites

This library should work with with Python 2.7.6 or later.

##Installation

Run ``python setup.py install``.

##Code Example

Here is a basic implementation of the library:

```python
from ircbot import bot

# Initialize the bot
# (The syntax is: server, port, username)
mybot = bot.Bot('chat.freenode.net', 6697, 'ChatBot') # You can specify extra arguments to set things like password, real name, etc.

# Connect
mybot.conn()

# Join a channel 
mybot.join('#channel')

# Speak in the channel
mybot.comm.messageChannel('This is a Test!','#channel')
```

To add your own command, you will need to create your own function. Your function needs to take 5 parameters: self, sender, channel, cmd, and params. Here's an example:

```python
def slap(self, sender, channel, cmd, params):
	message = 'slaps ' + (params.split(' ')[0] or sender) + " around a bit with a large trout"
	self.comm.perform_action(message, channel)
mybot.add_cmd('slap',slap)
```
