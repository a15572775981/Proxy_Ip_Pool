from .my_settings_proxy import *
from .my_redis_db import RedisClient
from .my_crawler_ip import Crawler


class Getter:
    """将存储模块和获取模块组织在一起"""
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """判断代理池上限"""
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        """"""
        print('获取器开始执行')
        if not self.is_over_threshold():  # 如果没有达到上限
            for callback_label in range(self.crawler.__CrawlFuncCount__):   # self.crawler.__CrawlFuncCount__获取crawl_方法数量
                callback = self.crawler.__CrawlFunc__[callback_label]  # self.crawler.__CrawlFunc__[callback_label]挨个调用crawl_方法
                proxies = self.crawler.get_proxies(callback)  # 将方法名字传入crawler_ip文件中的 get_proxies方法，让它去调用对应的craler方法得到IP地址
                for proxy in proxies:   # 将每个方法得到的列表当中的IP一个个添加到Redis数据库中
                    self.redis.add(proxy)