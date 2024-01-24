from functools import wraps
import inspect
import logging
import os
import sys

DEFAULT_FILENAME = "favorite.log"


def initialize_logging(console_level=logging.DEBUG,
                       file_level=logging.DEBUG,
                       filename=DEFAULT_FILENAME, mode="w"):
    """ Return a root logger configured the way Tim likes it.

    Returned logger has console and file handlers configured to produce
    standardized output like this:

    2023-10-18 10:21:16,659 INFO     [root:32] Logging initialized.

    The columns line up to make visual scanning easy.

    Parameters
    ==========
    console_level : int
        default : logging.DEBUG
    file_level : int
        default : logging.DEBUG
    filename : str
        default : "favorite.log"

    Returns
    =======
    logger : instance(logging.Logger)
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fmt = "%(asctime)s %(levelname)-8.8s [%(name)s:%(lineno)s] %(message)s"
    formatter = logging.Formatter(fmt)
    if len(logger.handlers) > 0:
        stream_handler = logger.handlers[0]
    else:
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
    stream_handler.setLevel(console_level)
    stream_handler.setFormatter(formatter)

    fp = open(filename, mode)
    file_handler = logging.StreamHandler(fp)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)

    logger.info("Logging initialized.  View Log file at "
                "{!r}".format(os.path.abspath(fp.name)))
    return logger


def log_args(logger, level=logging.DEBUG, is_method=False):
    """Decorator to log arguments passed to func."""
    def inner_func(func):

        @wraps(func)
        def return_func(*args, **kwargs):
            arg_log_fmt = "{name}({arg_str})"
            arg_list = []
            if is_method:  # get class name from arg[0]
                class_name = args[0].__class__.__name__
                arg_log_fmt = class_name + "." + arg_log_fmt
                if len(args) > 1:
                    arg_list.extend("{!r}".format(arg) for arg in args[1:])
            else:
                arg_list.extend("{!r}".format(arg) for arg in args)
            arg_list.extend("{}={!r}".format(key, val)
                            for key, val in kwargs.items())
            msg = arg_log_fmt.format(name=func.__name__,
                                     arg_str=", ".join(arg_list))
            # set stacklevel=2 to get lineno from the file defining
            # the function being wrapped, not this file.  Needs Python >= 3.8
            logger.log(level, msg, stacklevel=2)
            return func(*args, **kwargs)
        return return_func
    return inner_func


if __name__ == "__main__":
    initialize_logging()
    logger = logging.getLogger(__name__)

    @log_args(logger)
    def foo(x, y, z):
        pass

    class Bar(object):
        @log_args(logger, is_method=True)
        def baz(self, *args, **kwargs):
            pass

    foo(1, 2, z=3)

    bar = Bar()
    bar.baz(1, c=3, b=2)
    bar.baz()
