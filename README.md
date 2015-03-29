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

## Requirements

npyscreen 4.8.5 or later

## Author

Mark Tearle <mark@tearle.com>
