# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-07 19:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=32)),
                ('token', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='token')),
                ('department', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='部门')),
                ('tel', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='座机')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='手机')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('valid_begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_end_time', models.DateTimeField(blank=True, null=True)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'verbose_name': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('securitydevice', '机房设备'), ('software', '软件资产')], default='server', max_length=64)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('management_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('trade_date', models.DateField(blank=True, null=True, verbose_name='购买时间')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='过保修期')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='价格')),
                ('status', models.SmallIntegerField(choices=[(0, '在线'), (1, '已下线'), (2, '未知'), (3, '故障'), (4, '备用')], default=0)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='资产管理员')),
            ],
            options={
                'verbose_name_plural': '资产总表',
                'verbose_name': '资产总表',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='业务线')),
                ('memo', models.CharField(blank=True, max_length=64, verbose_name='备注')),
                ('parent_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_level', to='assets.BusinessUnit')),
            ],
            options={
                'verbose_name_plural': '业务线',
                'verbose_name': '业务线',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='合同号')),
                ('name', models.CharField(max_length=64, verbose_name='合同名称')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('price', models.IntegerField(verbose_name='合同金额')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='合同详细')),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('license_num', models.IntegerField(blank=True, verbose_name='license数量')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '合同',
                'verbose_name': '合同',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, max_length=128, verbose_name='CPU型号')),
                ('cpu_count', models.SmallIntegerField(verbose_name='物理cpu个数')),
                ('cpu_core_count', models.SmallIntegerField(verbose_name='cpu核数')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': 'CPU部件',
                'verbose_name': 'CPU部件',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('slot', models.CharField(max_length=64, verbose_name='插槽位')),
                ('manufactory', models.CharField(blank=True, max_length=128, null=True, verbose_name='制造商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘型号')),
                ('capacity', models.FloatField(verbose_name='磁盘容量GB')),
                ('iface_type', models.CharField(choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('SSD', 'SSD')], default='SAS', max_length=64, verbose_name='接口类型')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '硬盘',
                'verbose_name': '硬盘',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='事件名称')),
                ('event_type', models.SmallIntegerField(choices=[(1, '硬件变更'), (2, '新增配件'), (3, '设备下线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线\\更新\\变更'), (7, '其它')], verbose_name='事件类型')),
                ('component', models.CharField(blank=True, max_length=255, null=True, verbose_name='事件子项')),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='事件时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='事件源')),
            ],
            options={
                'verbose_name_plural': '事件纪录',
                'verbose_name': '事件纪录',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='机房名称')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '机房',
                'verbose_name': '机房',
            },
        ),
        migrations.CreateModel(
            name='Manufactory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufactory', models.CharField(max_length=64, unique=True, verbose_name='厂商名称')),
                ('support_num', models.CharField(blank=True, max_length=30, verbose_name='支持电话')),
                ('memo', models.CharField(blank=True, max_length=128, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '厂商',
                'verbose_name': '厂商',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '路由器'), (1, '交换机'), (2, '负载均衡'), (4, 'VPN设备')], default=0, verbose_name='服务器类型')),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VlanIP')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='设置详细配置')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '网络设备',
                'verbose_name': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('asset_type', models.CharField(blank=True, choices=[('server', '服务器'), ('switch', '交换机'), ('router', '路由器'), ('firewall', '防火墙'), ('storage', '存储设备'), ('NLB', 'NetScaler'), ('wireless', '无线AP'), ('software', '软件资产'), ('others', '其它类')], max_length=64, null=True)),
                ('manufactory', models.CharField(blank=True, max_length=64, null=True)),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('ram_size', models.IntegerField(blank=True, null=True)),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True)),
                ('cpu_count', models.IntegerField(blank=True, null=True)),
                ('cpu_core_count', models.IntegerField(blank=True, null=True)),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('os_release', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='资产数据')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='汇报日期')),
                ('approved', models.BooleanField(default=False, verbose_name='已批准')),
                ('approved_date', models.DateTimeField(blank=True, null=True, verbose_name='批准日期')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='批准人')),
            ],
            options={
                'verbose_name_plural': '新上线待批准资产',
                'verbose_name': '新上线待批准资产',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡名')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='网卡型号')),
                ('macaddress', models.CharField(max_length=64, unique=True, verbose_name='MAC')),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('netmask', models.CharField(blank=True, max_length=64, null=True)),
                ('bonding', models.CharField(blank=True, max_length=64, null=True)),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '网卡',
                'verbose_name': '网卡',
            },
        ),
        migrations.CreateModel(
            name='RaidAdaptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('slot', models.CharField(max_length=64, verbose_name='插口')),
                ('model', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('model', models.CharField(max_length=128, verbose_name='内存型号')),
                ('slot', models.CharField(max_length=64, verbose_name='插槽')),
                ('capacity', models.IntegerField(verbose_name='内存大小(MB)')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': 'RAM',
                'verbose_name': 'RAM',
            },
        ),
        migrations.CreateModel(
            name='SecurityDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '防火墙'), (1, '入侵检测设备'), (2, '互联网网关'), (4, '运维审计系统')], default=0, verbose_name='服务器类型')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'PC服务器'), (1, '刀片机'), (2, '小型机')], default=0, verbose_name='服务器类型')),
                ('created_by', models.CharField(choices=[('auto', 'Auto'), ('manual', 'Manual')], default='auto', max_length=32)),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('raid_type', models.CharField(blank=True, max_length=512, null=True, verbose_name='raid类型')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统类型')),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True, verbose_name='发型版本')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统版本')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
                ('hosted_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_on_server', to='assets.Server')),
            ],
            options={
                'verbose_name_plural': '服务器',
                'verbose_name': '服务器',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'OS'), (1, '办公\\开发软件'), (2, '业务软件')], default=0, verbose_name='服务器类型')),
                ('license_num', models.IntegerField(verbose_name='授权数')),
                ('version', models.CharField(help_text='eg. CentOS release 6.5 (Final)', max_length=64, unique=True, verbose_name='软件/系统版本')),
            ],
            options={
                'verbose_name_plural': '软件/系统',
                'verbose_name': '软件/系统',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Tag name')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='firmware',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Software'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.BusinessUnit', verbose_name='所属业务线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Contract', verbose_name='合同'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.IDC', verbose_name='IDC机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufactory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Manufactory', verbose_name='制造商'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(blank=True, to='assets.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'macaddress')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'slot')]),
        ),
    ]
