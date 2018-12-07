from functools import lru_cache


class TCException(Exception):
    pass


def _base(last, now, lap, offset, attr):
    '''
    last - last datetime
    now - current datetime
    lap - at what point to "roll over"
    offset - how many seconds between laps
    attr - what to look at
    '''
    # last started before :X, so if now > :X
    diff = round(now.timestamp(), 0) - round(last.timestamp(), 0)
    min_gap = offset - getattr(last, attr)
    if diff > offset:
        print('b3', attr)
        return True

    if getattr(last, attr) < lap:
        if getattr(now, attr) > lap:
            print('b1', attr)
            return True
        print('b2', attr)
        return False

    # last started after :X, so if now > last + interval, or if now > :X
    elif getattr(now, attr) > lap and diff > min_gap:
        print('b4', attr)
        return True
    print('b5', attr)
    return False


def _secondly(last, now, secondly):
    return _base(last, now, secondly, 60, 'second')


def _minutely(last, now, minutely):
    return _base(last, now, minutely, 3600, 'minute')


def _hourly(last, now, hourly):
    return _base(last, now, hourly, 3600*24, 'hour')


def _daily(last, now, daily):
    return _base(last, now, daily, 3600*24*7, 'day')


def _weekly(last, now, weekly):
    return _base(last, now, weekly, 3600*24*7*4.34, 'week')  # FIXME # of weeks should be derived from calendar


def _monthly(last, now, monthly):
    return _base(last, now, monthly, 3600*24*365, 'month')


def should_expire(last, now, secondly=None, minutely=None, hourly=None, daily=None, weekly=None, monthly=None, maxsize=128):
    '''should the cache expire?
    last - datetime
    now - datetime

    if yearly:
        necessary_distance = calc(0, 0, 0, 0, 0, 0, yearly)
    '''
    sec_res = _secondly(last, now, secondly) if secondly is not None else True
    min_res = _minutely(last, now, minutely) if minutely is not None else True
    hou_res = _hourly(last, now, hourly) if hourly is not None else True
    dai_res = _daily(last, now, daily) if daily is not None else True
    wee_res = _weekly(last, now, weekly) if weekly is not None else True
    mon_res = _monthly(last, now, monthly) if weekly is not None else True
    return all((sec_res, min_res, hou_res, dai_res, wee_res, mon_res))


@lru_cache(1000)
def calc(seconds=0, minutes=0, hours=0, days=0, weeks=0, months=0, years=0):
    return seconds + \
           minutes*60 + \
           hours*60*60 + \
           days*24*60*60 + \
           weeks*7*24*60*60 + \
           months*30*7*24*60*60 + \
           years*365*24*60*60
