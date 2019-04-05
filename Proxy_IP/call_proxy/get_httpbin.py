import requests
from study_crawler.Proxy_IP.call_proxy.call_proxies import get_proxies

def get_html():
    """测试看代理是否成功"""
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    url = 'http://httpbin.org/get'
    html = requests.get(url, proxies=get_proxies(), headers=headers)
    print(html.text)

get_html()