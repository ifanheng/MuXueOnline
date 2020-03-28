# Generated by Django 2.2.11 on 2020-03-20 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200318_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='is_auth',
            field=models.BooleanField(default=False, verbose_name='是否认证'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='is_gold',
            field=models.BooleanField(default=False, verbose_name='是否为金牌'),
        ),
    ]
