import datetime
import os
import re
import time
import sys

from bs4 import BeautifulSoup

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import django

from concurrent.futures import ThreadPoolExecutor

import requests
from lxml import etree
from queue import Queue
from utils.helper import get_text

from utils.validator import verify_ip, verify_baidu

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProxyIPPool.settings')
django.setup()

from IPPool.models import ProxyIP

# 创建队列
q = Queue()

# 创建更新队列
update_q = Queue()

# 创建av队列
baidu_q = Queue()


def crawl_89ip(page_count=2):
    """
    获取 http://www.89ip.cn/index.html 免费代理
    :param page_count:
    :return:
    """
    print(str(datetime.datetime.now()) + ' 开始爬取89ip......')
    start_url = 'http://www.89ip.cn/index_{}.html'
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    p89_ip_list = []
    for url in urls:
        headers = {
            "Referer": url,
            "Host": "www.89ip.cn",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url, options=headers)
        if response_html:
            tree = etree.HTML(response_html)
            tr_list = tree.xpath('//table[@class="layui-table"]/tbody/tr')
            for tr in tr_list:
                ip = tr.xpath("./td[1]/text()")[0].replace('\n', '').replace('\t', '')
                port = tr.xpath("./td[2]/text()")[0].replace('\n', '').replace('\t', '')
                q.put((ip, port))
                p89_ip_list.append((ip, port))
    # print(q.queue)
    # print(p89_ip_list)
    return p89_ip_list


def crawl_qy_dai_li(page_count=2):
    """
    获取旗云代理http://www.qydaili.com/free/?action=china&page=1
    :param page_count:
    :return:
    """
    print(str(datetime.datetime.now()) + ' 开始爬取qy......')
    start_url = "http://www.qydaili.com/free/?action=china&page={}"
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    qy_ip_list = []
    for url in urls:
        headers = {
            "Referer": url,
            "Host": "www.qydaili.com",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url)
        # 没有加入, options=headers，加了之后会出现Exceeded 30 redirects的错误

        if response_html:
            tree = etree.HTML(response_html)
            tr_list = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
            for tr in tr_list:
                try:
                    # proxy_type = tr.xpath("./td[4]/text()")[0].lower()
                    ip = tr.xpath("./td[1]/text()")[0]
                    port = tr.xpath("./td[2]/text()")[0]
                    q.put((ip, port))
                    qy_ip_list.append((ip, port))
                except:
                    continue
    return qy_ip_list


def crawl_3366_dai_li(page_count=5, stype='1'):
    """
    获取云代理http://www.ip3366.net/free/?stype=1&page=3
    :param page_count:
    :return:
    """
    print(str(datetime.datetime.now()) + ' 开始爬取3366代理......')
    start_url = "http://www.ip3366.net/free/?stype%s=1&page={}" % stype
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    ip_3366_list = []
    for url in urls:
        headers = {
            "Host": "www.ip3366.net",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url, options=headers)
        if response_html:
            tree = etree.HTML(response_html)
            tr_list = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
            for tr in tr_list:
                # proxy_type = tr.xpath("./td[4]/text()")[0].lower()
                ip = tr.xpath("./td[1]/text()")[0]
                port = tr.xpath("./td[2]/text()")[0]
                q.put((ip, port))
                ip_3366_list.append((ip, port))
    return ip_3366_list


def crawl_highanon():
    """
    http://www.proxylists.net/http_highanon.txt
    :return:
    """
    print(str(datetime.datetime.now()) + ' 开始爬取highanon......')
    url = 'http://www.proxylists.net/http_highanon.txt'
    response_html = get_text(url=url)
    hig_ip_list = []
    if response_html:
        tem = response_html.split('\n')
        for i in tem:
            if i == '':
                continue
            try:
                ip_port = i.split(':')
                hig_ip_list.append((ip_port[0], ip_port[1].replace('\r', '')))
                q.put((ip_port[0], ip_port[1].replace('\r', '')))
            except:
                return []
    return hig_ip_list


def crawl_66ip(page_count=2):
    """
    爬取http://www.66ip.cn/{}.html
    """
    print(str(datetime.datetime.now()) + ' 开始爬取66ip......')
    start_url = 'http://www.66ip.cn/{}.html'
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    sixsix_ip_list = []
    for url in urls:
        headers = {
            "Referer": url,
            "Host": "www.66ip.cn",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url, options=headers)
        if response_html:
            pattern = re.compile("<tr><td>(\d+.\d+.\d+.\d+)</td><td>(\d+)</td>", re.S)
            proxy_list = re.findall(pattern, response_html)
            for proxy in proxy_list:
                ip = proxy[0]
                port = proxy[1]
                ip = ip.strip()
                port = port.strip()
                q.put((ip, port))
                sixsix_ip_list.append((ip, port))
    return sixsix_ip_list


def craw_rmccurdy():
    """
    https://www.rmccurdy.com/scripts/proxy/good.txt
    暂时没法使用
    :return:
    """
    print(str(datetime.datetime.now()) + ' 开始爬取rmccurdy......')
    url = 'https://www.rmccurdy.com/scripts/proxy/good.txt'
    response_html = get_text(url=url)
    rmccurdy_ip_list = []
    if response_html:
        tem = response_html.split('\n')
        for i in tem:
            if i == '' or i == ':':
                continue
            try:
                ip_port = i.split(':')
                proxy_type = 'http'
                rmccurdy_ip_list.append((proxy_type, ip_port[0], ip_port[1]))
                q.put((ip_port[0], ip_port[1].replace('\r', '')))
            except:
                return []
    return rmccurdy_ip_list


def run_crawler():
    """
    爬取代理ｉｐ
    :return:
    """
    # craw_ip_list 为爬取各个免费代理ｉｐ的上面写的函数，当需要增加时，需要在这里面添加
    # craw_ip_list = [crawl_89ip, crawl_qy_dai_li, crawl_3366_dai_li, crawl_highanon, craw_rmccurdy]
    # craw_ip_list = [crawl_qy_dai_li(1), crawl_89ip(1)]
    # 把爬取函数添加到list中的时候，就开始执行爬取函数了，并且是按顺序爬取的

    with ThreadPoolExecutor(max_workers=4) as pool1:  # 创建一个最大容纳数量为4的线程池
        # for future in craw_ip_list:
        #     pool1.submit(future)
        crawler1 = pool1.submit(crawl_qy_dai_li, 3)  # # 通过submit提交执行的函数到线程池中
        crawler2 = pool1.submit(crawl_89ip, 3)
        crawler3 = pool1.submit(crawl_3366_dai_li, 3)
        crawler4 = pool1.submit(crawl_highanon)
        crawler5 = pool1.submit(crawl_66ip, 3)

    with ThreadPoolExecutor(max_workers=8) as pool2:
        """
        get_result 为用add_done_callback()方法来添加回调函数，该回调函数形如 fn(future)。当线程任务完成后，
        程序会自动触发该回调函数，并将对应的 Future 对象作为参数传给该回调函数
        """
        def get_result(future):
            proxy_info = future.result()

            if proxy_info:
                # 如果数据存在存入数据
                protocol = proxy_info.get('protocol', None)
                # types = proxy_info.get('types', None)
                ip = proxy_info.get('ip', None)
                port = proxy_info.get('port', None)
                speed = proxy_info.get('speed', None)

                proxy_ip = ProxyIP.objects.filter(protocol=protocol, ip=ip, port=port).first()
                if not proxy_ip:
                    proxy_ip = ProxyIP(ip=ip, port=port, protocol=protocol, speed=speed)
                    proxy_ip.save()
                    print('save: ' + str(proxy_ip))
                else:
                    print('already exist: ' + str(proxy_ip))

        while not q.empty():
            proxy_ip_port = q.get()  # ('112.12.37.196', '53281')  # get方法会把第一个元素pop出，并返回
            q.task_done()  # 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
            pool2.submit(verify_ip, proxy_ip_port[0], proxy_ip_port[1]).add_done_callback(get_result)

    q.join()  # 等到队列为空，再执行别的操作
    print('done')


def update_ip():
    """
    定期检测数据的可用性
    :return:
    """
    def check_ip(ip, port):
        proxy_info = verify_ip(ip, port)
        db_ip = ProxyIP.objects.filter(ip=ip, port=port).first()
        if proxy_info:
            db_ip.save()
        else:
            db_ip.delete()

    proxy_all = ProxyIP.objects.all()
    for proxy_info in proxy_all:
        update_q.put(proxy_info)

    with ThreadPoolExecutor(max_workers=8) as pool3:
        while not update_q.empty():
            proxy_info = update_q.get()  # pop出队首的代理
            update_q.task_done()  # 给队列一个信号
            pool3.submit(check_ip, proxy_info.ip, proxy_info.port)


def update_baidu_connection():
    """
    定期检测连接网站的状态
    """
    def check_ip(protocol, ip, port):
        baidu_connection = verify_baidu(protocol, ip, port)
        db_ip = ProxyIP.objects.filter(ip=ip, port=port).first()
        if baidu_connection:
            db_ip.score = 100
            db_ip.save()
            print(str(ip) + ':' + str(port) + ' 连接baidu成功')
        else:
            db_ip.score -= 1
            db_ip.save()
            print(str(ip) + ':' + str(port) + ' 连接baidu失败，分数减1')
            if db_ip.score <= 0:
                db_ip.delete()
                print('删除' + str(ip) + ':' + str(port))

    proxy_all = ProxyIP.objects.all()
    for proxy_info in proxy_all:
        baidu_q.put(proxy_info)

    with ThreadPoolExecutor(max_workers=8) as pool4:
        while not baidu_q.empty():
            proxy_info = baidu_q.get()
            baidu_q.task_done()
            pool4.submit(check_ip, proxy_info.protocol, proxy_info.ip, proxy_info.port)
