# Tim's Logging Setup

Over time I have developed a preferred setup for logging, using tips from friends & coworkers (like [Simon](https://stackoverflow.com/users/1250580/simon-jagoe) and [Tony](https://stackoverflow.com/users/260303/tony-s-yu)) and the kindness of strangers at [Stack Overflow](https://stackoverflow.com/q/32443808/1001165).  I've posted that implementation here for my own use and to share with friends and students.  Hope it helps!

Key features include a format string that makes searching and sorting easy and an argument-logging decorator that automatically logs the arguments a decorated function was called with.