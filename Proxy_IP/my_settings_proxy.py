# 储存模块
MAX_SCORE = 100   # 最大分数，可以代理分数
MIN_SCORE = 0   # 最小分数，移除代理分数
INITIAL_SCORE = 10   # 新获取代理分数
REDIS_HOST = 'localhost'  # redis库的IP地址
REDIS_PORT = 6379   # redis库的端口
REDIS_PASSWORD = None   # 登录redis的密码
REDIS_KEY = 'MyProxies'  # redis库里面的对应的键

# 获取IP
POOL_UPPER_THRESHOLD = 10000  # 设置IP数量最大值

# 检测模块
VALID_STATUS_CODES = [200]
TEST_URL = 'https://www.lagou.com/'  # 目标网站修改
BATCH_TEST_SIZE = 100

# 调度模块
TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# API 地址
API_HOST = '0.0.0.0'
API_PORT = 8888
