"""
运行python run.py 开始定时抓取代理ｉｐ和检测代理ｉｐ
在服务器中可以运行　nohup python -u run.py >> crawler.out 2>&1 &  在后台运行
"""
import logging

from ProxyIPPool.settings import CRAWLER_TIME, UPDATE_BAIDU_CONN_TIME
from utils.crawler import run_crawler, update_baidu_connection
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='log/log.txt', filemode='a')


def run():
    print('开启定时任务')
    scheduler = BlockingScheduler()
    scheduler.add_job(func=run_crawler, trigger='interval', minutes=CRAWLER_TIME)  # 每20分钟抓取一次
    scheduler.add_job(func=update_baidu_connection, trigger='interval', minutes=UPDATE_BAIDU_CONN_TIME)  # 每隔30min测试一次baidu连接
    scheduler._logger = logging
    scheduler.start()


if __name__ == '__main__':
    # 刚运行后20分钟后才开始抓取，所以要刚启动记忆开始抓取
    run_crawler()  # 先抓取代理
    run()  # 再开启定时任务
