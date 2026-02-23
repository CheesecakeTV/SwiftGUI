import logging
import logging.handlers
import sys
import time

class MemoryHandlerLevelOnly(logging.handlers.MemoryHandler):
    """
    Super obvious if you think about it
    """

    def shouldFlush(self, record):
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)
        return record.levelno >= self.flushLevel

#logging.RootLogger(logging.CRITICAL)
logging.basicConfig()
logging.getLogger().handlers[0].setLevel(logging.CRITICAL)

my_logger = logging.getLogger("SwiftGUI")
#my_logger.addHandler(logging.NullHandler())

my_handler = logging.StreamHandler(sys.stderr)
#my_logger.addHandler(my_handler)

my_buffer = MemoryHandlerLevelOnly(
    5,
    flushLevel= logging.ERROR,
    target=my_handler,
    flushOnClose=False,
)
my_logger.addHandler(my_buffer)

#my_format = logging.Formatter("")

for i in range(15):
    my_logger.warning(f'Test-log {i}')
    print("Hi")
    time.sleep(0.5)

my_logger.critical('ALARM')

