# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-23 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
        ('appconf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='serverList',
            field=models.ManyToManyField(blank=True, to='assets.Asset', verbose_name='所在服务器'),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appconf.AppOwner', verbose_name='产品线负责人'),
        ),
    ]
