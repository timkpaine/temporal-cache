import datetime
from mock import patch, MagicMock
from tempfile import NamedTemporaryFile


class TestExpire:
    def setup(self):
        self._olddatetime = datetime.datetime

        class NewDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                ret = self._now + self._delay
                print(self._now)
                print(ret)
                return ret

        datetime.datetime = NewDateTime

    def teardown(self):
        datetime.datetime = self._olddatetime

    def test_blank(self):
        from random import random
        from temporalcache import expire

        self._now = datetime.datetime(2018, 1, 1, 1, 1, 0)
        self._delay = datetime.timedelta(seconds=0)

        with NamedTemporaryFile() as f:
            @expire(1, persistent=f.name, maxsize=2)
            def foo(test):
                return random()

            print('running first')
            x = foo('a')
            print('checking cached')
            assert x == foo('a')
            foo('b')
            foo('c')
            x = foo('d')

            # expire
            self._delay = datetime.timedelta(seconds=2)
            print('checking cache expired')
            assert x != foo('d')
            print('success')