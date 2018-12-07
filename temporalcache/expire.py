import datetime
from functools import wraps, lru_cache
from .utils import should_expire


def expire(second=None, minute=None, hour=None, day=None, week=None, month=None, maxsize=128):
    '''Expires all entries in the cache @ whole number time

        for example, @expire(0, 30, 16) will expire the cache at 4:30pm every day
    '''
    if not any((second is not None, minute is not None, hour is not None, day is not None, week is not None, month is not None)):
        second = 0

    def _wrapper(foo):
        last = datetime.datetime.now()

        foo = lru_cache(maxsize)(foo)

        @wraps(foo)
        def _wrapped_foo(*args, **kwargs):
            nonlocal last

            now = datetime.datetime.now()
            if should_expire(last, now, second, minute, hour, day, week, month):
                foo.cache_clear()

            last = now
            return foo(*args, **kwargs)
        return _wrapped_foo
    return _wrapper
