#!/usr/bin/evn python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import datetime
import urllib
import sys


# 使用bs4进行数据的爬取
def get_domain_info(k,i):
    result=[]
    if 'http://' in  i :
        i = i[7:]
        
    # This 以下有两个url的处理，是因为域名的有效期在whois站才能获取最新的，在seo站只能获取以前的，有可能不是最新的，所以需要爬取两个页面的数据
    url = 'http://seo.chinaz.com/{}'.format(i)
    req = urllib.request.Request(url=url)
    req_data = urllib.request.urlopen(req)
    text = req_data.read()
    soup = BeautifulSoup(text, 'html.parser')
    
    # This url2只获取域名的过期时间，不获取其他的信息
    url2 = 'http://whois.chinaz.com/{}'.format(i)
    req2 = urllib.request.Request(url=url2)
    req_data2 = urllib.request.urlopen(req2)
    text2 = req_data2.read()
    soup2 = BeautifulSoup(text2, 'html.parser')
    
    # This 获取一些必有的信息，如域名时间、ip、ip来源
    try:
        ret_time = soup.find('div', class_='w97-0 brn col-hint02 pl0').text.split('于')[1].split(',')
        domain_age = soup.find('div', class_='w97-0 brn col-hint02 pl0').text.split('（')[0]
        ctime = ret_time[0][:-1].replace('年', '-').replace('月', '-')+ ' 00:00'
        #etime = ret_time[1].split('为')[1][:-2].replace('年', '-').replace('月', '-')+ ' 00:00'
        etime = soup2.find_all('li', class_='clearfix bor-b1s bg-list')[2].text.split('间')[1].replace('年', '-').replace('月', '-').replace('日', '')+ ' 00:00'
        lis = soup.find('div', class_='brn ipmW').text
        lis_ip = (lis[3:].split('['))[0]
        ip_source = (lis[3:].split('['))[1].split(']')[0]
    
        # This 获取完一些必有信息之外，再获取一些可能有的信息，因为有些域名可能没有备案，没有备案的就没有以下的信息
        # This 获取备案号
        try:
            domain_record_num = soup.find('a', href = re.compile("type=")).text
        except Exception as e:
            domain_record_num = '暂无信息'
        
        # This 判断是否备案，如果备案的话，strong标签就大于2的 
        domain_record = soup.findAll('strong')
        if len(domain_record) > 2:
            domain_record = soup.findAll('strong')
            domain_nature = domain_record[0].text
            domain_company = domain_record[1].text
        # This 如果没有备案，则备案信息相关的则显示 暂无信息
        else:
            #print("没有IP", e)
            domain_record = '暂无信息'
            domain_nature = '暂无信息'
            domain_company = '暂无信息'
    
    # This 如果没有获取到一些必有的信息的话，那就是域名不存在，就返回暂无信息
    except Exception as e:
        #print("域名没查到",e)
        domain_age = '暂无信息'
        ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        etime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        lis_ip = '0.0.0.0'
        ip_source = '暂无信息'
        domain_record_num = '暂无信息'
        domain_nature = '暂无信息'
        domain_company = '暂无信息'
            
            
    all_results = {'name':i, 'ip_source':ip_source, 'ip':lis_ip, 'ctime':ctime, 'etime':etime, 'domain_age':domain_age, 'domain_record_num':domain_record_num, 'domain_nature':domain_nature, 'domain_company':domain_company, 'comment':k}
    result.append(all_results)
    # This 执行这个刷新是因为在开发过程中，即使填写了不同的域以及域名，但是这个接口返回来的仍是上一个域的信息，所以存在缓存，需要进行刷新
    sys.stdout.flush()
    return result

    
