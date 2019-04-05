from flask import Flask, g
from .my_redis_db import RedisClient


__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):  # hasattr判断 g 类里面有没有 redis这个属性
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>My Proxy</h2>'

@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()
