#!/usr/bin/env python

# EXAMPLE using npyscreenreactor

import npyscreen
import curses

# Twisted

from twisted.internet import protocol
import npyscreenreactor

# Incorporates code
# from http://www.binarytides.com/python-socket-server-code-example/
# Socket server in python using select function
import socket, select

class MyTestApp(npyscreen.StandardApp):
    def updateFields(self, received="", sent=""):
	self.sent = sent
	self.received = received


    # socket code
    def onStart(self):
	self.keypress_timeout_default = 1
        self.addForm("MAIN",       MainForm, name="Screen 1", color="IMPORTANT",)
        self.addForm("SECOND",     MainForm, name="Screen 2", color="WARNING",  )
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
        self.add(npyscreen.TitleText, name = "Text:", value= "Press ^T to change screens" )
        self.sentfield = self.add(npyscreen.TitleText, name = "Sent:", value="", editable=False )
        self.receivedfield = self.add(npyscreen.TitleText, name = "Received:", value="", editable=False )
        
        self.add_handlers({"^T": self.change_forms})

    def while_waiting(self):
	self.sentfield.value = self.parentApp.sent
	self.receivedfield.value = self.parentApp.received
	self.sentfield.display()
	self.receivedfield.display()

    def on_ok(self):
        # Exit the application if the OK button is pressed.
        self.parentApp.switchForm(None)

    def change_forms(self, *args, **keywords):
        if self.name == "Screen 1":
            change_to = "SECOND"
        else:
            change_to = "MAIN"

        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
        
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
	response = 'OK ... ' + data
	self.transport.write(response)

	# update fields
	self.factory.app.updateFields(data,response)
     
    def connectionMade(self):
	response = "Hello there ...\n"
	data = "Connection from " + str(self.transport.getPeer())

	self.transport.write(response)
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

      
