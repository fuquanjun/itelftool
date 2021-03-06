#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from setup import views, ansible, shell, jobs, filetransfer, fileupload, record


urlpatterns = [
    # This shell功能模块开始
    url(r'^shell/$', shell.index, name='shell'),
    url(r'^scripts/exec/$', shell.exec_scripts, name='exec_scripts'),
    # This shell功能模块结束
    
    # This 文件上传功能模块开始
    url(r'^fileupload/$', fileupload.index, name='fileupload'),
    url(r'^fileupload/exec/$', fileupload.fileupload_result, name='fileupload_result'),
    # This 文件上传功能模块结束
    
    # This 文件分发功能模块开始
    url(r'^filetransfer/$', filetransfer.index, name='filetransfer'),
    url(r'^filetransfer/exec/$', filetransfer.exec_filetransfer, name='exec_filetransfer'),
    # This 文件分发功能模块结束
    
    # This ansible功能模块开始
    url(r'ansible/$', ansible.index, name='ansible'),
    url(r'^playbook/$', ansible.playbook, name='playbook'),
    url(r'^ansible/command/$', ansible.ansible_command, name='acommand'),
    url(r'^host/sync/$', ansible.host_sync, name='host_sync'),
    # This ansible功能模块结束
    
    # This 任务编排（定时任务）功能模块开始
    url(r'^job/list/$', jobs.index, name='job_list'),
    url(r'^job/add/$', jobs.job_add, name='job_add'),
    url(r'^job/del/$', jobs.job_del, name='job_del'),
    url(r'^job/edit/(?P<ids>\d+)/$', jobs.job_edit, name='job_edit'),
    url(r'^job/interval/list/$', jobs.job_interval_list, name='job_interval_list'),
    url(r'^job/interval/add/$', jobs.job_interval_add, name='job_interval_add'),
    url(r'^job/interval/del/$', jobs.job_interval_del, name='job_interval_del'),
    url(r'^job/interval/edit/(?P<ids>\d+)/$', jobs.job_interval_edit, name='job_interval_edit'),
    url(r'^job/crontab/list/$', jobs.job_crontab_list, name='job_crontab_list'),
    url(r'^job/crontab/add/$', jobs.job_crontab_add, name='job_crontab_add'),
    url(r'^job/crontab/del/$', jobs.job_crontab_del, name='job_crontab_del'),
    url(r'^job/crontab/edit/(?P<ids>\d+)/$', jobs.job_crontab_edit, name='job_crontab_edit'),
    url(r'^job/result/list/$', jobs.job_result_list, name='job_result_list'),
    url(r'^job/result/del/$', jobs.job_result_del, name='job_result_del'),
    url(r'^job/backend/$', jobs.job_backend, name='job_backend'),
    url(r'^job/backend/task/(?P<name>\w+)/(?P<action>\w+)$', jobs.job_backend_task, name='job_backend_task'),
    url(r'^job/result/edit/(?P<ids>\d+)/$', jobs.job_result_edit, name='job_result_edit'),
    # This 任务编排（定时任务）功能模块开始
    
    # This 任务编排操作记录模块开始
    url(r'^record/list/$', record.record_list, name='record_list'),
    url(r'^record/export/$', record.record_export, name='record_export'),
    # This 任务编排操作记录模块结束
]