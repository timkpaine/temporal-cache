from mock import patch, MagicMock


class TestConfig:
    def setup(self):
        pass
        # setup() before each test method

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        pass
        # setup_class() before any methods in this class

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test_daily(self):
        from temporalcaching import daily
        daily(None)

    def test_seconds(self):
        import time
        from random import random
        from temporalcaching import seconds

        @seconds(1)
        def foo():
            return random()

        print('running first')
        x = foo()
        print('checking cached')
        assert x == foo()

        # expire
        time.sleep(2)
        print('checking cache expired')
        assert x != foo()
        print('success')
