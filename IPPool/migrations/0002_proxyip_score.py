# Generated by Django 2.2 on 2020-03-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IPPool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxyip',
            name='score',
            field=models.IntegerField(default=10, verbose_name='得分'),
        ),
    ]
