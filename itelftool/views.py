#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
import django
from django import utils
from assets.dashboard import AssetDashboard
from django.contrib.auth.decorators import login_required
from assets.myauth import UserProfile
import time, datetime
import re
from assets.myauth import LoginRecord
from assets.models import Asset
from assets.models import EventLog
from broken_record.models import BrokenRrecord


# 首页模块
# 打开首页需要先进行登录，使用了django自带的login_required装饰器
@login_required
def index(request):
    # This 登录记录相关 开始
    date_time = datetime.datetime.now()
    login_record = LoginRecord.objects.filter(logintime__month=date_time.month)
    usercount = UserProfile.objects.all().count()
    login_user = []
    for i in login_record:
        if i.name not in login_user:
            login_user.append(i.name)
    login_user_count = len(login_user)  
    user_activity = '{:.0f}'.format(login_user_count/usercount*100)
    # This 登录记录相关 结束
    
    # This 服务器在线相关 开始
    assetcount = Asset.objects.all().count()
    asset_on_count = Asset.objects.filter(status=0).count()
    asset_on_rate = '{:.0f}'.format(asset_on_count/assetcount*100)
    # This 服务器在线相关 结束
    
    # This 故障率相关 开始
    broken_record = BrokenRrecord.objects.filter(occur_time__month=date_time.month)
    impact_time = 0
    for i in broken_record:
        a = int(i.business_impact_time.split(u'分')[0])
        impact_time += a
    business_impact_time_rate = '{:.2f}'.format((impact_time/(date_time.day*24*60))*100)
    # This 故障率相关 结束
    
    # This 资产变更率相关 开始
    even_change = EventLog.objects.filter(date__month=date_time.month)
    even_change_id = []
    for i in even_change:
        if i.asset not in even_change_id:
            even_change_id.append(i.asset)
    even_change_count= len(even_change_id)
    even_change_count_rate = '{:.2f}'.format(even_change_count/assetcount*100)
    # This 资产变更率相关 结束
    
    
    results = {
        'user_activity': user_activity,
        'asset_on_rate': asset_on_rate,
        'business_impact_time_rate': business_impact_time_rate,
        'even_change_count_rate': even_change_count_rate,
        'usercount': usercount,
        'assetcount': assetcount,
    }
    return render(request,'index.html', results)


# 登录验证模块
def acc_login(request):
    # 如果请求的方式为POST，则为提交账号密码的操作
    if request.method == "POST":
        vcode = request.POST.get('vcode')
        session_code = request.session['verifycode']
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        # 判断用户的账号密码是否验证通过
        if user is not None:
            # 判断用户输入的验证码是否正确
            if vcode.upper() == session_code:
                # valid_end_time这个是账户的有效期结束时间
                if user.valid_end_time: #设置了end time
                    # 秋飞修改
                    #if django.utils.timezone.now() > user.valid_begin_time and django.utils.timezone.now()  < user.valid_end_time:
                    # 如果当前的时间大于账号的有效开始时间，并且当前时间小于用户的有效结束时间，就登录成功
                    if utils.timezone.now() > user.valid_begin_time and utils.timezone.now()  < user.valid_end_time:
                        auth.login(request,user)
                        # 这个很重要，是设置用户登录后session保存多久，这里设置了30分钟，30分钟后需要重新登录
                        request.session.set_expiry(60*300)
                        #print 'session expires at :',request.session.get_expiry_date()
                        # This 用户登录记录到数据库
                        user = request.user
                        ipaddr = request.META['REMOTE_ADDR']
                        LoginRecord.objects.create(loginsource=ipaddr, name=user)
                        # 验证通过，返回首页
                        return HttpResponseRedirect('/')
                    else:
                        # 如果验证没通过，则返回登录页后，提示过期信息
                        return render(request,'login.html',{'login_err': '您的账号已过期，请联系管理员！'})
                # 秋飞修改
                #elif django.utils.timezone.now() > user.valid_begin_time:
                # 如果没有设置过期结束时间，那么则会查看当前时间是否比账号生效开始时间大，如果大就可以登录
                elif utils.timezone.now() > user.valid_begin_time:
                        auth.login(request,user)
                        # 这个很重要，是设置用户登录后session保存多久，这里设置了30分钟，30分钟后需要重新登录
                        request.session.set_expiry(60*300)
                        # This 用户登录记录到数据库
                        user = request.user
                        ipaddr = request.META['REMOTE_ADDR']
                        LoginRecord.objects.create(loginsource=ipaddr, name=user)
                        return HttpResponseRedirect('/')
            else:
                return render(request,'login.html',{'login_err': '您输入的验证码错误，请重新输入！'})

        # 如果页面提交过来的账号密码没通过验证，则提示账号或者密码错误
        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    # 如果请求的方式不是post，那么直接返回login.html页面，也就是登录页
    else:
        return render(request, 'login.html')

# 账号退出模块    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

# 后台用户信息里面，指定id修改指定用户的密码功能，由于用户认证写过了，如果还用原来的密码修改请求url，则会多一个change字段，需要把这个change字段删除，才能正常修改密码
def urlchange_passwd(request,userid):
    request_path = request.path.replace('/change','')
    return HttpResponseRedirect(request_path)

# 检查密码复杂度
def check_password(passwd):
    if re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])\w{6,}$',passwd):
        print("password %s correct" % passwd)
        return True
    else:
        print("password %s is invalid" % passwd)
        return False


# 前端用户修改密码功能
@login_required
def changepwd(request):
    if request.method == 'GET':
        return render(request, 'changepwd.html')
    else:
            username = request.user
            oldpassword = request.POST.get('old_password')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword1 = request.POST.get('new_password1')
                newpassword2 = request.POST.get('new_password2')
                result = check_password(newpassword1)
                if result is True:
                    if newpassword1 == newpassword2:
                        user.set_password(newpassword1)
                        user.save()
                        return HttpResponse("密码修改成功！<a href='/'>返回首页</a>")
                    else:
                        return render(request,'changepwd.html',{'changepwd_err': '您输入的两次新密码不匹配，请重新输入！'})
                else:
                    return render(request,'changepwd.html',{'changepwd_err': '密码必须由6个或以上的普通字符组成，必须有一个或以上英文数字，一个或以上英文字母！'})
            else:
                return render(request,'changepwd.html',{'changepwd_err': '原密码输入错误，请重新输入！'})
            
# 前端个人中心功能
@login_required
def userinfo(request):
    username = request.user
    userInfo = UserProfile.objects.get(email=username)
    #print(userInfo.last_login)
    return render(request,'userinfo.html',{'userinfo': userInfo})
    
