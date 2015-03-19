#ircbot

This is an IRC library for Python that abstracts away the lower level details of interacting with an IRC server. You can use this library to automate IRC tasks or create a bot. This library uses SSL by default.

This project was created to learn more about IRC and the IRC protocol.  I have found that it can be quite useful for creating an IRC bot or to perform similar tasks.  I have found [twisted](https://pypi.python.org/pypi/Twisted)'s implementation to be more efficient, particularly with networking.  I have found that it lacks features that this project has implemented however.

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
