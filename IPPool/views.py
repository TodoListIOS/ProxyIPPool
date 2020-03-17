from django.http import JsonResponse, HttpResponse

# Create your views here.
from IPPool.models import ProxyIP


def index(requests):
    """
    返回到说明页
    :param requests:
    :return:
    """
    context = '<h3>1.访问接口http://{运行服务器的ip}/api/fetch/ 随机返回一个代理ip信息</h3> <br/>' \
              '<h3>2.访问接口http://{运行服务器的ip}/api/random/{个数}, 随机返回指定个数</h3> <br/>' \
              '<h3>3.访问接口http://{运行服务器的ip}/api/count, 返回可用的代理数量</h3> <br/>'
    return HttpResponse(context)


def fetch(requests):
    """
    随机返回一个ip信息
    :param requests:
    :return:
    """
    # proxy_info = ProxyIP.objects.order_by('?').first()
    # proxy_info = ProxyIP.objects.filter(score=100).first()
    proxy_info = ProxyIP.objects.filter(score=100).order_by('?')[:1]  # 随机获取一条数据
    proxy_info = proxy_info[0]
    if proxy_info:
        data = {
            'code': '200',
            'msg': 'success',
            'ip_info': {
                'protocol': proxy_info.protocol,
                'ip': proxy_info.ip,
                'port': proxy_info.port,
                'speed': proxy_info.speed,
                'score': proxy_info.score,
                'verify_time': proxy_info.verify_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    else:
        data = {
            'code': '200',
            'msg': 'Data is empty',
            'ip_info': ''
        }
    return JsonResponse(data)


def random(requests, num):
    """
    随机返回num个数个ip
    :param requests:
    :param num:
    :return:
    """
    try:
        n = int(num)
    except ValueError:
        n = 1
    # ip_info_list = ProxyIP.objects.order_by('?')[:n]
    ip_info_list = ProxyIP.objects.filter(score=100)[:n]
    ip_info = []
    for proxy_info in ip_info_list:
        ip_info.append({
            'protocol': proxy_info.protocol,
            'ip': proxy_info.ip,
            'port': proxy_info.port,
            'speed': proxy_info.speed,
            'score': proxy_info.score,
            'verify_time': proxy_info.verify_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    data = {
        'code': '200',
        'msg': 'success',
        'ip_info': ip_info
    }
    return JsonResponse(data)


def count(requests):
    """
    返回代理池中可用的ip个数
    """
    ip_num = ProxyIP.objects.filter(score=100).count()
    data = {
        'code': 200,
        'msg': 'success',
        'ip_num': ip_num
    }
    return JsonResponse(data)
