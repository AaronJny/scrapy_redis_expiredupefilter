# -*- coding: utf-8 -*-
# @File  : setup.py
# @Author: AaronJny
# @Date  : 2018/12/17
# @Desc  :

from pkgutil import walk_packages
from setuptools import setup


def find_packages(path):
    # This method returns packages and subpackages as well.
    return [name for _, name, is_pkg in walk_packages([path]) if is_pkg]


setup(
    name="scrapy-redis-expiredupefilter",
    version="0.1.99",
    keywords=['scrapy', 'redis', 'expire', 'dupefilter', 'expiredupefilter'],
    description="A distributed crawler component based on scrapy_redis "
                "which can specify the expiration time of fingerprints in dupefilter.",
    license='MIT',
    author="AaronJny",
    author_email="aaronjny@163.com",
    url="https://blog.csdn.net/aaronjny",
    packages=list(find_packages('src')),
    package_dir={'': 'src'},
    include_package_data=True,
)
