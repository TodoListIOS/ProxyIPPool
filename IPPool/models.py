from django.db import models


# Create your models here.
class ProxyIP(models.Model):
    """
    可用代理ip信息
    """
    protocol = models.CharField(default='', max_length=10, verbose_name='代理类型')
    ip = models.CharField(max_length=16, null=True, verbose_name='ip')
    port = models.CharField(max_length=12, null=True, verbose_name='端口号')
    speed = models.CharField(max_length=12, null=True, verbose_name='响应速度')
    verify_time = models.DateTimeField(auto_now=True, verbose_name='最后验证时间')
    score = models.IntegerField(default=100, verbose_name='得分')  # 能入库的都是连接成功的，所以默认分数为100

    def __str__(self):
        return '{' + self.ip + ':' + self.port + ', speed:' + self.speed + '}'

    class Meta:
        db_table = 'proxy_ip'

