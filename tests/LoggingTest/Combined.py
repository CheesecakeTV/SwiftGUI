#import logging
import logging.handlers
import time
import traceback
import sys
from typing import Callable

class MemoryHandlerLevelOnly(logging.handlers.MemoryHandler):
    """
    Super obvious if you think about it
    """

    def shouldFlush(self, record):
        if len(self.buffer) > self.capacity:    # Remove 0th element so the buffer doesn't "overflow"
            self.buffer.pop(0)
        return record.levelno >= self.flushLevel

def reroute_exceptions(
        logger: logging.Logger = logging.getLogger(),
        loglevel: int = logging.CRITICAL,
        *,
        logger_warnings: logging.Logger = None,
        loglevel_warnings: int = logging.WARNING,
        reraise: bool = False,
        print_to_console: bool = False,
        pass_text_to_function: Callable[[str], ...] = None,
):
    """
    Catch all unhandled exceptions and log them

    :param logger: The logger where EXCEPTIONS go
    :param loglevel: The loglevel for EXCEPTIONS
    :param logger_warnings: The logger where WARNINGS go
    :param loglevel_warnings: The level of logging for WARNINGS
    :param reraise: True, if the exception should be raised again
    :param pass_text_to_function: Pass a function/method and the exception-text is passed to it
    :param print_to_console: True, if the text should be printed to the console using print(...)
    :return:
    """
    if logger_warnings is None:
        logger_warnings = logger

    if loglevel_warnings is None:
        loglevel_warnings = loglevel

    def catch(exctype, value, tb):
        nonlocal reraise
        text = "".join(traceback.format_exception(exctype, value, tb))

        if issubclass(exctype, Warning):    # Warnings
            print("WARNING!")
            if logger_warnings is not None:
                logger_warnings.log(
                    loglevel_warnings,
                    text,
                )
        elif issubclass(exctype, Exception):    # Real exceptions
            if logger is not None:
                logger.log(
                    loglevel,
                    text,
                )
        else:
            # Keyboard interrupts and such
            reraise = True

        if pass_text_to_function:
            pass_text_to_function(text)

        if print_to_console:
            print(text)

        if reraise:
            sys.__excepthook__(exctype, value, tb)

    sys.excepthook = catch

logging.basicConfig()

my_logger = logging.Logger("SwiftGUI", logging.DEBUG)
my_handler = logging.StreamHandler(sys.stderr)

my_buffer = MemoryHandlerLevelOnly(5, logging.CRITICAL, target=my_handler, flushOnClose=False)
my_logger.addHandler(my_buffer)

reroute_exceptions(logger=my_logger, reraise=False)

for i in range(10):
    print(i)
    my_logger.info(f"Hallo World {i}")
    time.sleep(0.25)

1 / 0
