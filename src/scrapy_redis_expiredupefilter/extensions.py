# -*- coding: utf-8 -*-
# @File  : extensions.py
# @Author: AaronJny
# @Date  : 2018/12/17
# @Desc  :

from . import get_redis_from_settings
import time
from . import defaults
from twisted.internet import task
from scrapy import signals
import logging


class ExpiredFingerprintCleaner:

    def __init__(self, server, key, interval):
        self.server = server
        self.key = key
        self.interval = interval
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        server = get_redis_from_settings(settings)
        dupefilter_key = settings.get("SCHEDULER_DUPEFILTER_KEY", defaults.SCHEDULER_DUPEFILTER_KEY)
        key = dupefilter_key
        interval = settings.get('EXPIRE_FIGGERPRINTS_CLEAN_INTERVAL', defaults.EXPIRE_FIGGERPRINTS_CLEAN_INTERVAL)
        instance = cls(server=server, key=key, interval=interval)
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(instance.spider_closed, signal=signals.spider_closed)
        return instance

    def spider_opened(self, spider):
        spider.logger.info('ExpiredFingerprintCleaner is Working!')
        self.key = self.key % {'spider': spider.name}
        self.tsk = task.LoopingCall(self.clean_expired_fingerprints)
        self.tsk.start(self.interval)

    def spider_closed(self, spider):
        if self.tsk.running:
            self.tsk.stop()
        spider.logger.info('ExpiredFingerprintCleaner is closed!')

    def clean_expired_fingerprints(self):
        x = self.server.zremrangebyscore(self.key, 0, int(time.time()))
        self.logger.info('{} fingerprints were cleaned up.'.format(x))
