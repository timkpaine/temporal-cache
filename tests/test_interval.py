import datetime
from mock import patch, MagicMock


class TestInterval:
    def setup(self):
        self._olddatetime = datetime.datetime
        _now = datetime.datetime.now()

        class NewDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                ret = _now + self._delay
                print(_now)
                print(ret)
                return ret

        datetime.datetime = NewDateTime

    def teardown(self):
        datetime.datetime = self._olddatetime

    def test_blank(self):
        from random import random
        from temporalcache import interval

        self._delay = datetime.timedelta(seconds=0)

        @interval()
        def foo():
            return random()

        print('running first')
        x = foo()
        print('checking cached')
        assert x == foo()

        # expire
        self._delay = datetime.timedelta(seconds=2)
        print('checking cache expired')
        assert x != foo()
        print('success')

    def test_seconds(self):
        from random import random
        from temporalcache import interval

        self._delay = datetime.timedelta(seconds=0)

        @interval(seconds=1)
        def foo():
            return random()

        print('running first')
        x = foo()
        print('checking cached')
        assert x == foo()

        # expire
        self._delay = datetime.timedelta(seconds=2)
        print('checking cache expired')
        assert x != foo()
        print('success')

    def test_minutes(self):
        from random import random
        import temporalcache
        self._delay = datetime.timedelta(seconds=0)

        @temporalcache.interval(minutes=1)
        def foo():
            return random()

        print('running first')
        x = foo()
        print('checking cached')
        assert x == foo()

        self._delay = datetime.timedelta(minutes=1, seconds=1)
        print('checking cache expired')
        assert x != foo()
        print('success')
