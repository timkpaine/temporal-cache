import datetime
from functools import wraps, lru_cache
from .utils import calc


def interval(seconds=0, minutes=0, hours=0, days=0, weeks=0, months=0, years=0, maxsize=128):
    '''Expires all entries in the cache every interval'''
    if not any((seconds, minutes, hours, days, weeks, months, years)):
        seconds = 1

    def _wrapper(foo):
        last = datetime.datetime.now()

        foo = lru_cache(maxsize)(foo)

        @wraps(foo)
        def _wrapped_foo(*args, **kwargs):
            nonlocal last

            now = datetime.datetime.now()
            if (now - last).seconds > calc(seconds, minutes, hours, days, weeks, months, years):
                foo.cache_clear()

            last = now
            return foo(*args, **kwargs)
        return _wrapped_foo
    return _wrapper
