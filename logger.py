import sys, os, signal
import time
from datetime import datetime
from pytz import timezone

class _Logger:
    """ Overall class for logging scrape events"""
    f = None
    
    
    
    def _write(self, text, level="5"):
        """Write a log event
            0 "Emergency"
            1 "Alert"
            2 "Critical"
            3 "Error"
            4 "Warning"
            5 "Notice"
            6 "Info"
            7 "Debug"
            8 "Trace"
        """
        if self.f is None:
            # lazily open log to get the app a chance to init
            self.f = self.open_log()

        if self.f is None:
            print(text)  # write to console if there is no file
        else:
            ts = self.get_ts()
            # print(ts)
            text = f"{ts} {level} {str(text)}\n"  # + " " + str(text) + "\n"

            try:
                self.f.write(text)
            except OSError as error:
                # reconnect to file
                self._handle_stale_file_error()

                # wait a second in case there is a network blip
                time.sleep(1)

                # try to write again. If we get another exception we want that to be thrown and to kill the job
                self.f.write(text)

            # also write to console
            print(text)

    def _handle_stale_file_error(self):
        """We appear to be losing the connection to the file on the NFS file system.
        This method will attempt to reconnect to the folder
        """
        print(f"WARN: Lost connection to logging file located {self._get_output_dir()}. Attempting to close and reconnect.")
        self.close()
        self.f = self.open_log()

    def notice(self, text):
        self._write(text=text, level="5")

    def info(self, text):
        self._write(text=text, level="6")

    def debug(self, text):
        self._write(text=text, level="7")

    def error(self, text):
        self._write(text=text, level="3")

    def warning(self, text):
        self._write(text=text, level="4")



# globally shared logger
_root = None


def notice(text):
    """Log a message of level 'notice'. Scraping Level 5

    Args:
        text (str): The message to log
    """
    global _root
    _root.notice(text)


def info(text):
    """Log a message of level 'info'. Scraping Level 6

    Args:
        text (str): The message to log
    """
    global _root
    _root.info(text)


def debug(text):
    """Log a message of level 'debug'. Scraping Level 7

    Args:
        text (str): The message to log
    """
    global _root
    _root.debug(text)


def error(text):
    """Log a message of level 'error'. Scraping Level 3

    Args:
        text (str): The message to log
    """
    global _root
    _root.error(text)


def warning(text):
    """Log a message of level 'warning'. Scraping Level 4

     Args:
            text (str): The message to log
    """
    global _root
    _root.warning(text)


def trace(text):
    """Log a message of level 'trace'. Use this instead of print(). This
    message only shows up when dev_mode = True and will not show up in the
    Scraping Logs

    Args:
        text (str): The message to log
    """
    global _root
    _root.trace(text)


def close():
    """Close the logger. This should not be called by script developers.
    """

    global _root
    _root.close()
    _root = None
    del _root