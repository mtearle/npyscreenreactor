#!/usr/bin/env python

# EXAMPLE-npyscreenreactor-client.py

# Copyright (c) 2015 Mark Tearle <mark@tearle.com>
# See LICENSE for details.

# This examples connects to localhost on port 5000
# 
# This can either be the matching server example:
#
#	EXAMPLE-npyscreenreactor-server.py
#
# or netcat:
#
#	nc -l -p 5000 127.0.0.1

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

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
        line='Connection made.\n\n' 
        self.app.lines_to_buffer(line)

    def lineReceived(self,line):
        self.app.line_to_buffer(line.decode("ascii"))

class TestClientFactory(protocol.ClientFactory):
    def __init__(self,app):
        self.app = app
        app.set_factory(self)
 
    def startedConnecting(self, connector):
        line='Started connecting'
        self.app.connector = connector
        #self.app.line_to_buffer(line)

    def buildProtocol(self, addr):
        line='Building protocol'
        self.instance = self.protocol(self.app)
        self.instance.delimiter = b'\n'
        self.app.set_instance(self.instance)
        self.instance.setLineMode()
        return self.instance

    def clientConnectionLost(self, connector, reason):
        self.app.connector = connector
        line="""
Lost connection.
Reason: %s

Type ^Q to exit, hit ENTER to (re) connect
""" % reason
        self.app.lines_to_buffer(line)

    def clientConnectionFailed(self, connector, reason):
        self.app.connector = connector
        line="""
Connection failed.
Reason: %s

Type ^Q to exit, hit ENTER to (re) connect
""" % reason
        self.app.lines_to_buffer(line)


class EditorFormExample(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.BufferPager

    def __init__(self, *args, **keywords):
        super(npyscreen.FormMutt, self).__init__(*args, **keywords)
        self.wCommand.add_handlers({
                        curses.ascii.NL : self.do_line,
                        curses.ascii.CR : self.do_line,
                        "^Q" : self.exit_application,
                })
        self.wMain.add_handlers({
                        "^Q" : self.exit_application,
                })

    def do_line(self,name):
        if self.parentApp.connector.state == "disconnected":
                self.parentApp.connector.connect()
        elif self.parentApp.connector.state == "connecting":
                pass
        else:
                self.parentApp.process_line()
                self.display()
  
    def afterEditing(self):
        self.parentApp.switchForm(None)

    def exit_application(self,name):
        self.parentApp.line_to_buffer("Quitting...")
        self.parentApp.switchForm(None)

class TestApp(npyscreen.StandardApp):
    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def onStart(self):
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
        self.instance.sendLine(self.F.wCommand.value.encode("ascii"))
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

