from .my_redis_db import RedisClient
import aiohttp
import asyncio
from .my_settings_proxy import *
import time


class Tester:
    """创建检测类"""
    def __init__(self):
        self.redis = RedisClient()

    async def single_proxy(self, proxy):
        """测试单个代理"""
        conn = aiohttp.TCPConnector(verify_ssl=False)  # 防止SSL证书错误
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):  # isinstance判断对象的类型
                    proxy = proxy.decode('utf-8')  # 如果是字节码类型就转成字符串
                real_proxy = 'http://' + proxy
                # print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:  # timeout:超时处理
                    if response.status in VALID_STATUS_CODES:  # VALID_STATUS_CODES状态码列表
                        self.redis.max(proxy)  # 如果用这个代理请求百度状态码是 200 ，那么就将它添加到数据库并且设置100分
                        print('代理可用:  ', proxy)
                    else:
                        self.redis.decrease(proxy)  # 分数-1，低于10分就移除
                        print('请求响应不合法', proxy)
            except Exception:
                self.redis.decrease(proxy)
                # print('代理请求失败', proxy)

    def run(self):
        """主函数"""
        print('测试器开始运作')
        try:
            proxies = self.redis.all()  # 获取全部代理
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):  # 每100个一个循环
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]  # 循环100个之间的单个代理,i:i 索引
                task = [self.single_proxy(proxy) for proxy in test_proxies]  # 将每100个代理打包成 task任务
                loop.run_until_complete(asyncio.wait(task))  # 将这些请求百度测试的任务扔到事件循环中
                time.sleep(5)
        except Exception as e:
            print('测试器错误', e.args)


