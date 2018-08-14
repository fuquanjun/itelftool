# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-10 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20180810_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='机柜')),
                ('desc', models.CharField(blank=True, max_length=100, verbose_name='描述')),
                ('idc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.IDC', verbose_name='所在机房')),
                ('serverList', models.ManyToManyField(blank=True, to='assets.Asset', verbose_name='所在服务器')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='服务器组名')),
                ('desc', models.CharField(blank=True, max_length=100, verbose_name='描述')),
                ('serverList', models.ManyToManyField(blank=True, to='assets.Asset', verbose_name='所在服务器')),
            ],
        ),
    ]