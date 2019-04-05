import re
from pyquery import PyQuery as pq
from .my_get_html import get_page


class ProxyMetaclass(type):
    """重写tpye父类的__new__方法"""
    def __new__(cls, name, bases, attrs):  # attrs:以字典形式存储所有这个类的属性和方法
        count = 0
        attrs['__CrawlFunc__'] = []  # 在这个类中新创建一个字典形式的属性，key 是__CrawlFunc__，value是一个空列表
        for k, v in attrs.items():  # 遍历这个字典
            if 'crawl_' in k:  # 如果以 crawl_ 开头的方法在Key里面
                attrs['__CrawlFunc__'].append(k)  # 那么就将这个方法的名称添加到新建的字典的value的列里面
                count += 1
        attrs['__CrawlFuncCount__'] = count  # 再新建一个字典，将有多少个代理的数量添加到里面
        return type.__new__(cls, name, bases, attrs)

class Crawler(metaclass=ProxyMetaclass):   # 将ProxyMetaclass定义为元类
    """获取代理类"""
    def get_proxies(self, callback):   # callback参数出入的是调用代理的结果
        """依次调用下面的代理解析方法并将结果以列表形式返回"""
        proxies = []
        for proxy in eval("self.{}()".format(callback)):  # eval：将字符串转换成有效的表达式
            # print('成功获取代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host':'www.xicidaili.com',
                'Referer':'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests':'1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')

    def crawl_yundaili(self):
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_31f(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }
        url = 'http://31f.cn/'
        html = get_page(url, options=headers)
        result = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>\s<td>(\d+)</td>', html, re.S)
        for res in result:
            ip_res = res[0] + ':' + res[1]
            yield ip_res.replace(' ', '')

    def crawl_89ip(self):
        for i in range(1, 11):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            result = re.findall('<tr>\s+<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>\s+<td>\s+(\d+)\s+</td>', html, re.S)
            for res in result:
                ip_res = res[0] + ':' + res[1]
                yield ip_res.replace(' ', '')

    def crawl_yqie(self):
        url = 'http://ip.yqie.com/ipproxy.htm'
        response = get_page(url)
        result = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>', response, re.S)
        for res in result:
            ip_res = res[0] + ':' + res[1]
            yield ip_res.replace(' ', '')

