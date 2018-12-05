from datetime import datetime
from functools import wraps, lru_cache
from .daily import daily


__version__ = '0.0.1'


def seconds(timeout=1):
    def _wrapper(foo):
        last = datetime.now()

        foo = lru_cache()(foo)

        @wraps(foo)
        def _wrapped_foo(*args, **kwargs):
            nonlocal last

            now = datetime.now()
            if (now - last).seconds > timeout:
                foo.cache_clear()

            last = now
            return foo(*args, **kwargs)
        return _wrapped_foo
    return _wrapper
