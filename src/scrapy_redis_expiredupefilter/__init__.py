# -*- coding: utf-8 -*-
from .connection import (  # NOQA
    get_redis,
    get_redis_from_settings,
)

"""
This package is modified based on scrapy_redis(author:Rolando Espinoza,version:0.7.0-dev).

I only modified a small piece of code in dupefilter.The rest of the code uses the 
original code of scrapy_redis.

Pay tribute to the original author.
"""

__author__ = 'AaronJny'
__email__ = 'aaronjny at 163.com'
__version__ = '0.1.9'
