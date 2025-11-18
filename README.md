# Tim's Logging Setup

Over time I have developed a preferred setup for logging, using tips from friends & coworkers (like [Simon](https://stackoverflow.com/users/1250580/simon-jagoe) and [Tony](https://stackoverflow.com/users/260303/tony-s-yu)) and the kindness of strangers at [Stack Overflow](https://stackoverflow.com/q/32443808/1001165).  I've posted that implementation here for my own use and to share with friends and students.  Hope it helps!

Key features include a format string that makes searching and sorting easy and an argument-logging decorator that automatically logs the arguments a decorated function was called with.

# Installation

## `pip install`
Make sure your desired Python environment is active, then type:
```
pip install "td_log @ git+https://github.com/timdiller/favorite_logging_setup"
```

## Install from source
Make sure your desired Python environment is active, then type:
```
$ git clone git@github.com:timdiller/favorite_logging_setup.git
$ cd favorite_logging_setup
$ pip install ./
```

# Quick Start
## Example Usage
```python
# demo.py
import logging
from td_log.util import initialize_logging, log_args


logger = logging.getLogger(__name__)


@log_args(logger)
def foo(x, y, z):
    pass


class Bar(object):
    @log_args(logger, is_method=True)
    def baz(self, *args, **kwargs):
        pass


if __name__ == "__main__":
    initialize_logging()

    foo(1, 2, z=3)

    bar = Bar()
    bar.baz(1, c=3, b=2)
    bar.baz()
```
Executing the above script yields the following output:
```
2024-05-15 14:46:40,573 INFO     [root:54] Logging initialized.  View Log file at '/path/to/favorite.log'
2024-05-15 14:46:40,573 DEBUG    [__main__:22] foo(1, 2, z=3)
2024-05-15 14:46:40,573 DEBUG    [__main__:25] Bar.baz(1, c=3, b=2)
2024-05-15 14:46:40,574 DEBUG    [__main__:26] Bar.baz()
```