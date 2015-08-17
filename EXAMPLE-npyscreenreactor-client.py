#!/usr/bin/env python
import curses

import npyscreen
import npyscreenreactor

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver


class TestProtocol(LineReceiver):
    """This is just about the simplest possible protocol"""

    def __init__(self, app, *args, **keywords):
        self.app = app

    def connectionMade(self):
        line='Connection made.' 
        self.app.line_to_buffer(line)
	self.sendLine("Connection from example .... ")

    def lineReceived(self,line):
	self.app.line_to_buffer(line)

class TestClientFactory(protocol.ClientFactory):
    def __init__(self,app):
        self.app = app
	app.set_factory(self)
 
    def startedConnecting(self, connector):
        line='Started connecting'
	print line
	#self.app.line_to_buffer(line)

    def buildProtocol(self, addr):
        line='Building protocol'
        self.instance = self.protocol(self.app)
	self.instance.delimiter = "\n"
	self.app.set_instance(self.instance)
	self.instance.setLineMode()
        return self.instance

    def clientConnectionLost(self, connector, reason):
        line='Lost connection.  Reason: %s' % reason
        self.app.line_to_buffer(line)

    def clientConnectionFailed(self, connector, reason):
        line='Connection failed. Reason: %s' % reason
        self.app.line_to_buffer(line)


class EditorFormExample(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.BufferPager

    def __init__(self, *args, **keywords):
	super(npyscreen.FormMutt, self).__init__(*args, **keywords)
	self.wCommand.add_handlers({
			curses.ascii.NL : self.do_line,
			curses.ascii.CR : self.do_line,
		})

    def do_line(self,name):
	self.parentApp.process_line()
	self.display()
  
    def afterEditing(self):
        self.parentApp.switchForm(None)

class TestApp(npyscreen.StandardApp):
    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def onStart(self):
        factory = TestClientFactory(App)
        factory.protocol = TestProtocol
        self.reactor.connectTCP("127.0.0.1",5000,factory)
        self.F = self.addForm('MAIN', EditorFormExample)
        self.F.wStatus1.value = "Status Line "
        self.F.wStatus2.value = "Enter text to send ...."
	self.line_to_buffer("Hello cruel world ...")

    def when_exit(self,val):
        self.parentApp.switchForm(None)

    def line_to_buffer(self, line):
	self.F.wMain.buffer((line,))
	self.F.display()
	
    def process_line(self):
	self.instance.sendLine(self.F.wCommand.value)
	self.line_to_buffer(self.F.wCommand.value)
	self.F.wCommand.value = ""
	self.F.display()

    def set_reactor(self,reactor):
	self.reactor = reactor

    def set_factory(self,factory):
	self.factory = factory

    def set_instance(self,instance):
	self.instance = instance

#    def main(self):
#        
#        self.F.edit()


if __name__ == "__main__":
    App = TestApp()
    reactor = npyscreenreactor.install()
    reactor.registerNpyscreenApp(App)
    App.set_reactor(reactor)
    try:
        reactor.run()
    finally:
        reactor.stop()


####

# look at
# https://code.google.com/p/twisted-chat-example/source/browse/chatclient.py


#Spawn nc -lk 127.0.0.1 2000

#Spawn nc -l 127.0.0.1 2000
#on connection made you should see 'test line'
#on every COMMAND:VALUE from nc ('\r\n') , the VALUE should endup in npyscreen widget 'MSG'



