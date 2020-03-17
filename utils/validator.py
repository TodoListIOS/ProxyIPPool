import json
import time

import requests

from ProxyIPPool import settings


def verify_ip(proxy_ip, proxy_port):
    http_proxies = {
        "http": "http://%s:%s" % (proxy_ip, proxy_port),
    }
    https_proxies = {
        "https": "https://%s:%s" % (proxy_ip, proxy_port),
    }

    def _verify_test(test_url, proxy_protocol):
        if proxy_protocol.upper() == 'HTTP':
            proxies = http_proxies
        elif proxy_protocol.upper() == 'HTTPS':
            proxies = https_proxies

        try:
            _start = time.time()
            r = requests.get(url=test_url, headers=settings.BASE_HEADERS, proxies=proxies, timeout=5)
            if r.status_code == 200:
                speed = '%.2f秒' % (time.time() - _start)
                return True, speed  # 返回：测试成功，速度为speed
        except Exception as e:
            pass
        return False, 0  # 返回：测试失败，速度为0

    bai_du_test_url = settings.BAIDU_TEST_URL
    http_connect_success, http_connect_speed = _verify_test(test_url=bai_du_test_url, proxy_protocol='HTTP')
    https_connect_success, https_connect_speed = _verify_test(test_url=bai_du_test_url, proxy_protocol='HTTPS')

    if http_connect_success:
        protocol = 'HTTP'
        speed = http_connect_speed
    elif https_connect_success:
        protocol = 'HTTPS'
        speed = https_connect_speed
    else:  # https，http代理都无法连接成功时
        return None

    proxy_info = {
        "ip": proxy_ip,
        "port": proxy_port,
        "protocol": protocol,
        "speed": speed,
    }
    print(proxy_info)
    return proxy_info


def verify_baidu(proxy_protocol, proxy_ip, proxy_port):
    """
    测试代理链接av_url是否成功
    """
    proxies = {}
    if proxy_protocol == 1:  # http
        proxies = {"http": "http://%s:%s" % (proxy_ip, proxy_port)}
    elif proxy_protocol == 2:  # https
        proxies = {"https": "https://%s:%s" % (proxy_ip, proxy_port)}
    # proxies = {
    #     "http": "http://%s:%s" % (proxy_ip, proxy_port),
    #     "https": "https://%s:%s" % (proxy_ip, proxy_port),
    # }
    baidu_connection = False
    try:
        r = requests.get(url=settings.BAIDU_TEST_URL, proxies=proxies, timeout=5)
        if r.status_code == 200:
            baidu_connection = True
    except Exception as e:
        pass
    return baidu_connection
