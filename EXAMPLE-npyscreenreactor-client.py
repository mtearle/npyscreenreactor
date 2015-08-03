#!/usr/bin/env python
import npyscreen
import curses

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

# needs handler ....
# on enter ...

class TestApp(npyscreen.NPSApp):
    def process_line(self):
	self.F.wMain.buffer((self.F.wCommand.value,))
	self.F.wCommand.value = ""
	self.F.display()

    def main(self):
        self.F = EditorFormExample(parentApp=self)
        self.F.wStatus1.value = "Status Line "
        self.F.wStatus2.value = "Enter text to send ...."
	self.F.wMain.buffer(("boo\n", "book\n"))
	self.F.wMain.buffer(("boo\n", "book\n"))
        
        self.F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
