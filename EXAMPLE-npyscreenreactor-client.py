#!/usr/bin/env python

# EXAMPLE-npyscreenreactor-client.py

# This examples connects to localhost on port 5000
# 
# This can either be 
#    EXAMPLE-npyscreenreactor-server.py
# or
#    netcat:
#
#        nc -l 127.0.0.1 5000

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
	self.app.connected = True
        line='Connection made.\n\n' 
        self.app.lines_to_buffer(line)

    def lineReceived(self,line):
	self.app.line_to_buffer(line)

class TestClientFactory(protocol.ClientFactory):
    def __init__(self,app):
        self.app = app
	app.set_factory(self)
 
    def startedConnecting(self, connector):
        line='Started connecting'
	#self.app.line_to_buffer(line)

    def buildProtocol(self, addr):
        line='Building protocol'
        self.instance = self.protocol(self.app)
	self.instance.delimiter = "\n"
	self.app.set_instance(self.instance)
	self.instance.setLineMode()
        return self.instance

    def clientConnectionLost(self, connector, reason):
	self.app.connected = False
	self.app.connector = connector
        line='Lost connection.\n  Reason: %s\n' % reason
        self.app.lines_to_buffer(line)

    def clientConnectionFailed(self, connector, reason):
	self.app.connected = False
	self.app.connector = connector
        line='Connection failed.\n Reason: %s\n' % reason
        self.app.lines_to_buffer(line)


class EditorFormExample(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.BufferPager

    def __init__(self, *args, **keywords):
	super(npyscreen.FormMutt, self).__init__(*args, **keywords)
	self.wCommand.add_handlers({
			curses.ascii.NL : self.do_line,
			curses.ascii.CR : self.do_line,
		})

    def do_line(self,name):
	if not self.parentApp.connected:
		self.parentApp.connector.connect()
	else:
		self.parentApp.process_line()
		self.display()
  
    def afterEditing(self):
        self.parentApp.switchForm(None)

class TestApp(npyscreen.StandardApp):
    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def onStart(self):
	self.connected = False
	self.connector = None

	# connection details
	host = "127.0.0.1"
	port = 5000

	intro="""
%s

Welcome to the twisted npyscreen reactor client example.

Type ^Q to exit, hit ENTER to (re) connect

Connecting to %s on %s
...
""" % (__file__, host, port)

        factory = TestClientFactory(App)
        factory.protocol = TestProtocol
        self.reactor.connectTCP(host,port,factory)
        self.F = self.addForm('MAIN', EditorFormExample)
        self.F.wStatus1.value = "Status Line "
        self.F.wStatus2.value = "Enter text to send ...."
	self.lines_to_buffer(intro)
	# set initial focus
	# how to do this?
	

    def when_exit(self,val):
        self.parentApp.switchForm(None)

    def lines_to_buffer(self, lines):
	for line in lines.split("\n"):
		self.line_to_buffer(line)

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

if __name__ == "__main__":
    App = TestApp()
    reactor = npyscreenreactor.install()
    reactor.registerNpyscreenApp(App)
    App.set_reactor(reactor)
    try:
        reactor.run()
    finally:
        reactor.stop()


