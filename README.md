# 概述

scrapy-redis-expiredupefilter是基于scrapy-redis修改来的一款scrapy分布式爬虫框架，相比于scrapy-redis，它增加了一个小功能：你可以为每个请求的请求指纹设置指定的过期时间。

在scrapy-redis中，要么清空整个请求指纹集合，要么保留整个指纹集合，你无法为某个指纹设置生命周期（即TTL，Time-To-Live，让某个指纹在指定时间后自动清除）。scrapy-redis-expiredupefilter就是为了解决这个问题而出现的。

scrapy-redis-expiredupefilter只是在scrapy-redis上做了小小的修改，大部分代码依然使用scrapy-redis的原始代码。

向scrapy-redis的开发者致敬！

# 快速开始

**1.安装**

scrapy-redis-expiredupefilter的依赖与scrapy-redis完全相同，如果你已经安装了scrapy-redis，就不需要再考虑依赖问题。如果你没有安装，请参考requriments安装相关依赖或者直接安装scrapy-redis。

使用pip安装scrapy-redis-expiredupefilter:

```
python3 -m pip install scrapy-redis-expiredupefilter
```

**2.使用**

scrapy-redis-expiredupefilter的使用方法也与scrapy-redis几乎相同，只需要在settings里做简单的配置即可。

注意，当你使用scrapy-redis-expiredupefilter时，不需要再使用scrapy-redis，它集成了scrapy-redis中的所有功能（因为scrapy-redis-expiredupefilter只对scrapy-redis中关于指纹去重的部分进行了修改，并添加了定时批量清理过期指纹的扩展）。

你需要在settings中添加如下配置：

```
# 使用支持 TTL DUPEFILTER 调度器
SCHEDULER = 'scrapy_redis_expiredupefilter.scheduler.Scheduler'
# 带有 TTL 的 DUPEFILTER
DUPEFILTER_CLASS = 'scrapy_redis_expiredupefilter.dupefilter.RFPDupeFilter'
# REDIS连接
REDIS_URL = 'redis://:[your_ password]@your_host:your_port/your_db_num'
# 不清空数据
SCHEDULER_PERSIST = True
# 请求指纹的生命周期 TTL 不配置默认为86400,即一天
SCHEDULER_DUPEFILTER_EXPIRE_TIME = 86400 * 7
# 清理过期指纹的频率 默认60s一次
EXPIRE_FIGGERPRINTS_CLEAN_INTERVAL = 60
# 是否使用 DUPEFILTER DEBUG，默认False，设置为True则会显示dupefilter中的部分细节，便于调试
# DUPEFILTER_DEBUG = True
# 定期清理过期指纹的扩展，使用此扩展需要在EXTENSIONS中添加，建议使用，避免过期指纹产生积累
EXTENSIONS = {
    'scrapy_redis_expiredupefilter.extensions.ExpiredFingerprintCleaner': 100,
}
```

更多配置参考scrapy和scrapy-redis，scrapy-redis中有效的设置在scrapy-redis-expiredupefilter中也有效。

配置完毕，正常编写爬虫即可。

**3.定制**

你还可以为某些请求单独指定TTL，而不使用公用配置的`SCHEDULER_DUPEFILTER_EXPIRE_TIME`。你可以像下面这样处理：

在settings里配置：

```python
SCHEDULER_DUPEFILTER_EXPIRE_TIME = 86400 * 3
```

在spider中编写：

```python
# 这个请求的指纹将使用公用配置的SCHEDULER_DUPEFILTER_EXPIRE_TIME，3天内不重复采集
yield Request(url=url, callback=self.parse)
# 这个请求的指纹使用指定的request_expire_time，5天内不重复采集
yield Request(url=url, callback=self.parse_job, meta={'request_expire_time':86400*5})
```