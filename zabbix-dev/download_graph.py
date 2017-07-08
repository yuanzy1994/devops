#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from . import app, jsonrpc
#import util
import json
import traceback
import datetime
import cookielib
import urllib2
import urllib
import time

TIME = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


class Zabbix_api():

    def __init__(self, url="http://172.16.80.130:8888/index.php", name="admin", password="zabbix"):
        self.url = url
        self.name = name
        self.passwd = password
        # 初始化的时候生成cookies
        cookiejar = cookielib.CookieJar()
        urlOpener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookiejar))
        values = {"name": self.name, 'password': self.passwd,
                  'autologin': 1, "enter": 'Sign in'}
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        try:
            urlOpener.open(request, timeout=10)
            self.urlOpener = urlOpener
        except urllib2.HTTPError, e:
            print e

    def GetGraph(self, url="http://172.16.80.130:8888/chart2.php", values={'width': 800, 'height': 200, 'graphid': '680', 'stime': TIME, 'period': 3600}, image_dir="/tmp"):
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        url = self.urlOpener.open(request)
        image = url.read()
        imagename = "%s/%s_%s.jpg" % (image_dir,
                                      values["graphid"], values["stime"])
        f = open(imagename, 'wb')
        f.write(image)
        return 1
if __name__ == "__main__":
    graph = Zabbix_api()
    values = {'width': 800, 'height': 200, 'graphid': '569',
              'stime': TIME, 'period': 3600}
    graph.GetGraph("http://172.16.80.130:8888/chart2.php", values, "/tmp")
