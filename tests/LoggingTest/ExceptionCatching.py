import sys
import traceback


# Closely inspired by this post: https://stackoverflow.com/a/6234491
def catch(exctype, value, tb):
    print(exctype)
    print(value)
    print(tb)

    text = "".join(traceback.format_exception(exctype, value, tb))
    print(text)
    #logging.error("Unhandled exception: %s", text)

# Inspired by this post: https://stackoverflow.com/a/8168122
def test(exctype, value, tb):
    print(traceback.format_exception(exctype, value, tb))
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = test

1 / 0


