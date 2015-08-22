# twisted-reactor-npyscreen

##Twisted Reactor for npyscreen

In order to use this code, simply do the following::

    |  import npyscreenreactor
    |  npyscreenreactor.install()

Create a npyscreenApp; you will need to use npyscreen.StandardApp

Then, when your root npyscreenApp has been created::

    | from twisted.internet import reactor
    | reactor.registerNpyscreenApp(yourApp)
    | reactor.run()

Then use twisted.internet APIs as usual. 
Stop the event loop using reactor.stop()

##Code Explanation

The reactor subclasses Twisted's SelectReactor.  It requires use of
the new npyscreen StandardApp.  The reactor is iterated by a event 
(and associated callback) placed on the npyscreen App Queue that is called 
when the application processes it's event queue.

## Examples

There are two examples for the reactor provided; one a client, the other
a server.    They work together but can be run independently.

### EXAMPLE-npyscreenreactor-server.py

The example server listens on port 5000.  This can be connected to via telnet
or the example client.   Once a connection has been made, the server
responds to any text provided to it by prepending "OK .. " to the text
and responding.

### EXAMPLE-npyscreenreactor-client.py

The client connects to a server on localhost port 5000 (either the example
above or netcat).   Text can be typed in the bottom entry field and it
will be sent to the server.  Any text sent or received on a line by line
basis is displayed in the main pane.

## Contributions

Further contributions of examples are encouraged.

## Requirements

npyscreen 4.8.5 or later

## Author

Mark Tearle <mark@tearle.com>
