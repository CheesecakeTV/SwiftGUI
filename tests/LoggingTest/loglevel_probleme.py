import logging
import sys

logging.basicConfig()

# Log-level für normale Nachrichten setzen:
logging.getLogger().handlers[0].setLevel(logging.CRITICAL)

# Alternativ:
logging.getLogger().handlers.clear()
logging.getLogger().addHandler(logging.NullHandler())

my_logger = logging.getLogger("MyLogger")
my_logger.setLevel(logging.DEBUG)
#my_logger.addHandler(logging.StreamHandler(sys.stdout))

my_logger.warning('Test-log')


