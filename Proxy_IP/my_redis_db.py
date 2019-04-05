from study_crawler.Proxy_IP.my_settings_proxy import *
from random import choice  # 随机取一个元素
import redis


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host:IP
        :param port: 端口
        :param password:密码
        """
        # 下面定义连接Redis服务器，decode_response: redis默认取出的内容是字节，将原本的字节转换成字符串
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)  # 如果数据库中没有这个键值对，那么就添加到里面，并且给新的代理10分

    def random(self):
        """
        随机获取有效代理，首先尝试最高分，如果不存在，那么就按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)  # 返回有序集合中分数区间的所有元素，从小到大
        if len(result):  # 如果不为空
            return choice(result)  # 随机取一个100分数的代理
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)   # 有序集合中元素大到小排序
            if len(result):
                return choice(result)
            else:
                raise Exception('代理池枯竭')

    def decrease(self, proxy):
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理值
        """
        score = self.db.zscore(REDIS_KEY, proxy)   # 获取返回代理IP
        if score and score > MIN_SCORE:
            # print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)  # 有序集合中改变(增加)已有的值说对应的分数,如果该值不存在即新添加一个值
        else:
            # print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)  # 删除有序集合中的指定元素

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy:代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None  # 返回不为空的代理值

    def max(self, proxy):
        """
        将代理设置为 MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        # print('代理:', '[' + proxy + ']', '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)  # 将有序集合中的代理改成最高分数

    def count(self):
        """
        获取数量
        :return:数量
        """
        return self.db.zcard(REDIS_KEY)  # 返回有序集合中的元素个数

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)  # 返回有序集合中所有元素，由小到大

