# temporal-cache

Time-based cache invalidation

[![Build Status](https://github.com/timkpaine/temporal-cache/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/timkpaine/temporal-cache/actions?query=workflow%3A%22Build+Status%22)
[![Coverage](https://codecov.io/gh/timkpaine/temporal-cache/branch/main/graph/badge.svg?token=ag2j2TV2wE)](https://codecov.io/gh/timkpaine/temporal-cache)
[![License](https://img.shields.io/github/license/timkpaine/temporal-cache.svg)](https://pypi.python.org/pypi/temporal-cache/)
[![PyPI](https://img.shields.io/pypi/v/temporal-cache.svg)](https://pypi.python.org/pypi/temporal-cache/)
[![Docs](https://img.shields.io/readthedocs/temporal-cache.svg)](https://temporal-cache.readthedocs.io)


## Install

From pip

`pip install temporal-cache`

Or from source

`python setup.py install`

## Why?

I needed something that would automagically refresh at 4:00pm when markets close.

```python3

    @expire(hour=16)
    def fetchFinancialData():
    
```

## Interval Cache

The interval cache expires every `time` interval since its first use

```python3

    @interval(seconds=5, minutes=2)
    def myfoo():
        '''myfoo's lru_cache will expire 2 minutes, 5 seconds after last use'''
```


## Expire Cache

The expire cache expires on the time given, in scheduler/cron style.

```python3

    @expire(second=5, minute=2)
    def myfoo():
        '''myfoo's lru_cache will expire on the second minute, fifth second of every hour, every day, etc'''
```


## Caveats

Python hashing symantics persist. Dicts will be frozen, lists will be converted to tuples. Users are advised to pre-freeze to avoid issues.
