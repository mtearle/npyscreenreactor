import npyscreen
import npyscreenreactor


from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

#Spawn nc -l 127.0.0.1 2000
#on connection made you should see 'test line'
#on every COMMAND:VALUE from nc ('\r\n') , the VALUE should endup in npyscreen widget 'MSG'


class TestApp(npyscreen.StandardApp):

  def onCleanExit(self):
    npyscreen.notify_wait("Goodbye!")

  def while_waiting(self):
    pass
    #print 'app waiting'
    
  def onStart(self):
    self.addForm('MAIN', MainForm, name="testConnection")

  def while_waiting(self):
    pass

  def when_exit(self,val):
    self.parentApp.switchForm(None)

class MainForm(npyscreen.Form):
  def create(self):
    self.testWdg = self.add(npyscreen.TitleText, name='MSG', value='NONE',editable=False,color='CAUTIONHL')
  
  def afterEditing(self):
    self.parentApp.switchForm(None)
  
  def while_waiting(self):
    pass

class TestProtocol(LineReceiver):
  """This is just about the simplest possible protocol"""
  def connectionMade(self):
    #print 'Connection made.'
    self.sendLine("test line")
    self.setLineMode()

  def dataReceived(self,line):
    print line
    if line.startswith("COMMAND:"):
      self.factory.app.getForm("MAIN").testWdg.value=line.split(":")[1]
      self.factory.app.getForm("MAIN").testWdg.update()

class TestClientFactory(protocol.ClientFactory):
  def __init__(self,app):
    self.app = app
 
  def startedConnecting(self, connector):
    #print 'Started connecting'
    pass

  def buildProtocol(self, addr):
    #print 'Building protocol'
    proto = self.protocol()
    proto.factory = self
    return proto

  def clientConnectionLost(self, connector, reason):
    print 'Lost connection.  Reason: %s' % reason

  def clientConnectionFailed(self, connector, reason):
    print 'Connection failed. Reason: %s' % reason


if __name__ == "__main__":
  App = TestApp()
  factory = TestClientFactory(App)
  factory.protocol = TestProtocol
  reactor = npyscreenreactor.install()
  reactor.registerNpyscreenApp(App)
  reactor.connectTCP("127.0.0.1",2000,factory)
  try:
    reactor.run()
  finally:
    reactor.stop()
  