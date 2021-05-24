#! /usr/bin/python3

"""
pyloaders - Basic ASCII loaders for Python CLI programs
"""

import threading
import ctypes
import time
import sys

__version__ = "0.0.5"

class tc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class Loader(object):
    """
    Base Loader class. Contains the majority of class attributes as well as the
    core runtime methods. If the duration attribute is set, the pr() method is
    called after the chosen number to end the loader. If the loader is threaded
    (default), the run() method continues until termination with stop().
    """

    def __init__(self, text="Loading", size="medium", speed=.25, duration=None,
            direction="ltr", animation="loop", colour="", style="",
            complete_text="Done!", character="."):
        self.text = text
        self.size = size
        self.speed = speed
        self.duration = duration
        self.direction = direction
        self.animation = animation
        self.terminal_colour = str(colour).lower()
        self.terminal_style = str(style).lower()
        self.complete_text = complete_text
        self.character = character[:1]
        self.thread = None

    @property
    def colour(self):
        """
        Set string escape for terminal colour output (from colours package)
        """
        colours = {
            "": "",
            "blue": tc.OKBLUE,
            "green": tc.OKGREEN,
            "yellow": tc.WARNING,
            "orange": tc.WARNING,
            "red": tc.FAIL,
        }
        try:
            if str(self) == "Loader":
                return tc.FAIL
            return colours[self.terminal_colour]
        except:
            return ""

    @property
    def style(self):
        """
        Set string escape for terminal style output (from colours package)
        """
        styles = {
            "": "",
            "header": tc.HEADER,
            "bold": tc.BOLD,
            "underline": tc.UNDERLINE,
        }
        try:
            if str(self) == "Loader":
                return tc.BOLD
            return styles[self.terminal_style]
        except:
            return ""

    def __str__(self):
        """
        Print Loader class type
        """
        return self.__class__.__name__

    def draw(self, string):
        """
        Stylized print to console continuously while staying on the same line
        """
        sys.stdout.write("\r" + self.style + self.colour + string + tc.ENDC)
        sys.stdout.flush()
        if self.speed:
            time.sleep(self.speed)

    def pr(self):
        """
        Custom print method upon loader termination. Returns console output to normal.
        """
        sys.stdout.write("\r" + tc.BOLD + tc.OKGREEN + "[success]  " + tc.ENDC + self.complete_text + " " * 64)
        sys.stdout.flush()
        sys.stdout.write("\n")

    def run(self):
        """
        Run method for base loader class. Prints warning message then exits.
        """
        self.draw("WARNING: No child loader class selected")
        if self.duration:
            time.sleep(self.duration)
            self.pr()

    def start(self):
        """
        Start primary loader thread calling the run() method in the initialized loader class.
        """
        if not self.thread:
            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True
            self.thread = thread
            self.thread.start()
            return True
        else:
            return False


    def terminate(self):
        """
        Stop active loader thread if running.
        """
        if self.thread:
            if not self.thread.is_alive():
                return
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.thread.ident), exc)
            if res == 0:
                raise ValueError("nonexistent thread id")
            elif res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread.ident, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
            else:
                self.pr()
        else:
            raise ValueError("No thread to terminate")

    def stop(self):
        """
        Wrapper for terminate() class method.
        """
        if self.thread:
            self.terminate()
            self.thread = None
            return True
        else:
            sys.stdout.write("%s thread not started." % str(self))
            return False

class SpinningLoader(Loader):

    @property
    def characters(self):
        """
        List of ASCII characters for Spinning Loader.
        """
        return [u"\u2013", "\\", "|", "/"]

    def run(self):
        """
        Loop through character set, printing the next character and chosen
        loading message.
        """
        n = 0
        while True:
            if n == self.duration:
                self.pr()
                return
            else:
                for c in self.characters:
                    self.draw("[%s]          %s " % (c, self.text))
                n += 1

class TextLoader(Loader):

    def get_length(self):
        """
        Convert size attribute (small, medium, large) into respective number
        of characters.
        """
        if self.size.lower() == "large":
            length = len(self.text) + 16
        elif self.size.lower() == "medium":
            length = len(self.text) + 8
        else:
            length = len(self.text) + 4
        return length

    def run(self):
        """
        Mimic animated text by changing the number of '.' characters each side
        of the chosen message.
        """
        length = self.get_length()
        direction = self.direction
        text_length = len(self.text)
        start = int(((length - text_length) / 2) + 1)
        i = 0
        iter = self.duration if self.duration else 1
        while i < iter * (1 / self.speed):
            if self.duration:
                i += 1
            if direction.lower() == "ltr":
                start += 1
                if start > length - text_length:
                    if self.animation.lower() == "bounce":
                        direction = "rtl"
                        start -= 2
                if start >= length - 1:
                    start = 0
            else:
                start -= 1
                if start < 0:
                    if self.animation.lower() == "bounce":
                        direction = "ltr"
                        start = 1
                    else:
                        start = length - 1
            end = (start + text_length) % length
            self.direction = direction
            if start >= length - text_length:
                before_dots = ""
                after_dots = (length - text_length) * self.character
                left_text = self.text[::-1][:end][::-1]
                right_text = self.text[:length - start]
                center_text = ""
            else:
                before_dots = start * self.character
                after_dots = (length - end) * self.character
                left_text = ""
                right_text = ""
                center_text = self.text
            full_text = left_text + before_dots + center_text + after_dots + right_text
            self.draw(full_text + " ")
        if self.duration:
            self.pr()

class BarLoader(Loader):

    def __init__(self, character="=", *args, **kwargs):
        super(BarLoader, self).__init__(*args, **kwargs)
        self.character = character[:1]

    def get_length(self):
        """
        Convert size attribute (small, medium, large) into respective number
        of characters.
        """
        if self.size.lower() == "large":
            length = 100
        elif self.size.lower() == "medium":
            length = 50
        else:
            length = 20
        return length

    def run(self):
        """
        Mimic animated bar by changing the number of space characters each side
        of the bar.
        """
        length = self.get_length()
        direction = self.direction
        bar_length = int(length / 2)
        bar = self.character * bar_length
        start = int(((length - bar_length) / 2) + 1)
        i = 0
        iter = self.duration if self.duration else 1
        while i < iter * (1 / self.speed):
            if self.duration:
                i += 1
            if direction.lower() == "ltr":
                start += 1
                if start > length - bar_length:
                    if self.animation.lower() == "bounce":
                        direction = "rtl"
                        start -= 2
                if start >= length - 1:
                    start = 0
            else:
                start -= 1
                if start < 0:
                    if self.animation.lower() == "bounce":
                        direction = "ltr"
                        start = 1
                    else:
                        start = length - 1
            end = (start + bar_length) % length
            self.direction = direction
            if start >= length - bar_length:
                before_space = ""
                after_space = (length - bar_length) * " "
                left_bar = bar[::-1][:end][::-1]
                right_bar = bar[:length - start]
                center_bar = ""
            else:
                before_space = start * " "
                after_space = (length - end) * " "
                left_bar = ""
                right_bar = ""
                center_bar = bar
            full_bar = "|" + left_bar + before_space + center_bar + after_space + right_bar + "|"
            self.draw(full_bar + " ")
        if self.duration:
            self.pr()

class ProgressLoader(BarLoader):

    def __init__(self, start=0, total=100, *args, **kwargs):
        super(ProgressLoader, self).__init__(*args, **kwargs)
        self.start = start
        self.total = total
        self.speed = None

    def run(self):
        print("Progress Loader has no run method")
        return None

    def progress(self, current=None):
        """
        Each time this function is called, it reprints a bar loader with the
        length of the bar with the length of the bar proportional to the input
        'current' argument compared to the class 'total' attribute (default 100)
        """
        length = self.get_length()
        if not current:
            current = self.start
        # while current <= self.total:
        completion = (float(current) / float(self.total)) * 100
        percent = 100 if completion >= 100 else int(completion)
        filled = int(percent / (100 / length))
        done = self.character * filled
        remaining = " " * (length - filled)
        ascii = "\r|%s%s| %d%%" % (done, remaining, percent)
        self.draw(ascii)
        # current += 1
        if current >= self.total:
            time.sleep(.5)
            self.pr()
            return
