import requests



def get_proxy():
    """向web端获取随机IP"""
    url = 'http://127.0.0.1:8888/random'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None

def get_proxies():
    """以http或者https的格式返回"""
    try:
        proxy = get_proxy()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        return proxies
    except Exception:
        return None