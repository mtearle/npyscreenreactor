#!/usr/bin/env python

# EXAMPLE-npyscreenreactor-server.py

# Copyright (c) 2015 Mark Tearle <mark@tearle.com>
# See LICENSE for details.

# This example binds to localhost and listens on port 5000
#
# Any text received is responded with an "OK .. " followed by the text
#

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import npyscreen
import curses

# Twisted

from twisted.internet import protocol
import npyscreenreactor

class MyTestApp(npyscreen.StandardApp):
    def updateFields(self, received="", sent=""):
        self.sent = sent
        self.received = received

    def onStart(self):
        self.keypress_timeout_default = 1
        self.addForm("MAIN",       MainForm, name="EXAMPLE-npyscreenreactor-server", color="IMPORTANT",)
        self.sent=""
        self.currentform = None


    def while_waiting(self):
        pass

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
    
    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()
    
class MainForm(npyscreen.ActionForm):
    def create(self):
        self.keypress_timeout_default = 1
        self.sentfield = self.add(npyscreen.TitleText, name = "Sent:", value="", editable=False )
        self.receivedfield = self.add(npyscreen.TitleText, name = "Received:", value="", editable=False )
        
    def while_waiting(self):
        self.sentfield.value = self.parentApp.sent
        self.receivedfield.value = self.parentApp.received
        self.sentfield.display()
        self.receivedfield.display()

    def on_ok(self):
        # Exit the application if the OK button is pressed.
        self.parentApp.switchForm(None)


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    # helper method to do for python 3 unicode handling
    def writeToTransport(self, response):
        self.transport.write(response.encode("ascii"))
        
    def dataReceived(self, data):
        "As soon as any data is received, write it back."

	# for python 3, decode ascii stream to unicode
        response = 'OK ... ' + data.decode("ascii")
        self.writeToTransport(response)

        # update fields
        self.factory.app.updateFields(data,response)
     
    def connectionMade(self):
        response = "OK ... Hello there ...\n"
        data = "Connection from " + str(self.transport.getPeer())

        self.writeToTransport(response)
        self.factory.app.updateFields(data,response)

class EchoFactory(protocol.Factory):
    "factory for echo"

    # default protocol
    protocol = Echo

    def __init__(self, app):
        self.app = app

def main():
    testApp = MyTestApp()

    factory = EchoFactory(testApp)
    factory.protocol = Echo

    reactor = npyscreenreactor.install()
    PORT = 5000
    reactor.listenTCP(PORT,factory)
    testApp.updateFields(received="Chat server started on port " + str(PORT))

    reactor.registerNpyscreenApp(testApp)
    reactor.run()

if __name__ == '__main__':
    main()

      
