# Generated by Django 2.2.11 on 2020-03-24 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20200323_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=300, verbose_name='课程公告'),
        ),
    ]
