# -*- coding: utf-8 -*-
#coding=utf-8
import bs4 as bs
import urllib2

def urlOpen(url,loop=10):
    while loop>=1:
        loop -= 1
        if loop==9:
            print '打开连接 '+url
        else:
            print url+' 打开失败  第'+str(10-loop)+'次尝试'
        # url_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # header ={ 'User-Agent' : url_agent }
        # request=urllib2.Request(url,'',header)
        # responce=urllib2.urlopen(request,timeout=10)
        responce= urllib2.urlopen(url,timeout=10)
        html=responce.read()
        if html:
            break
    return html

