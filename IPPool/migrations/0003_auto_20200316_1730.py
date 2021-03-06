# Generated by Django 2.2 on 2020-03-16 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IPPool', '0002_proxyip_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxyip',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='proxyip',
            name='types',
        ),
        migrations.AlterField(
            model_name='proxyip',
            name='protocol',
            field=models.SmallIntegerField(choices=[(0, '未知'), (1, 'HTTP'), (2, 'HTTPS')], default=0, verbose_name='代理类型'),
        ),
    ]
