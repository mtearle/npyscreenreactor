#!/usr/bin/env python

# npyscreenreactory.py

# Inspired by pausingreactor.py and xmmsreactor.py

# npyscreen modifications

# Copyright (c) 2015 Mark Tearle <mark@tearle.com>
# See LICENSE for details.

"""
This module provides npyscreen event loop support for Twisted.

In order to use this support, simply do the following::

    |  import npyscreenreactor
    |  npyscreenreactor.install()

Then, when your root npyscreenApp has been created::

    | from twisted.internet import reactor
    | reactor.registerNpyscreenApp(yourApp)
    | reactor.run()

Then use twisted.internet APIs as usual. 
Stop the event loop using reactor.stop()

Maintainer: Mark Tearle
"""

from twisted.python import log, runtime
from twisted.internet import selectreactor

import npyscreen

class NpyscreenReactor(selectreactor.SelectReactor):
    """
    npyscreen reactor.

    npyscreen drives the event loop
    """
    def doIteration(self, timeout):
	# Executing what normal reactor would do...
	self.runUntilCurrent()

	selectreactor.SelectReactor.doIteration(self, timeout)

	# push event back on the npyscreen queue
	self.npyscreenapp.queue_event(npyscreen.Event("_NPYSCREEN_REACTOR"))

    def registerNpyscreenApp(self, npyscreenapp):
        """
        Register npyscreen.StandardApp instance with the reactor.
        """
        self.npyscreenapp = npyscreenapp
	# push an event on the npyscreen queue
	self.npyscreenapp.add_event_hander("_NPYSCREEN_REACTOR", self._twisted_events)

    def _twisted_events(self, event):
	self.doIteration(0)

    def _stopNpyscreen(self):
        """
        Stop the Npsycreen event loop if it hasn't already been stopped.

        Called during Twisted event loop shutdown.
        """
        if hasattr(self, "npyscreenapp"):
            self.npyscreenapp.setNextForm(None)

    def run(self,installSignalHandlers=True):
        """
        Start the reactor.
        """
	# Executing what normal reactor would do...
	self.startRunning(installSignalHandlers=installSignalHandlers)
 
	# do initial iteration and put event on queue to do twisted things 
	self.doIteration(0)

        # add cleanup events:
        self.addSystemEventTrigger("after", "shutdown", self._stopNpyscreen)

	#
        self.npyscreenapp.run()

def install():
    """
    Configure the twisted mainloop to be run inside the npyscreen mainloop.
    """
    reactor = NpyscreenReactor()
    from twisted.internet.main import installReactor
    installReactor(reactor)
    return reactor


__all__ = ['install']
