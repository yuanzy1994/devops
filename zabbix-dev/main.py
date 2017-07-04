#-*-coding:utf-8-*-

import json
import urllib2
from urllib2 import URLError
import sys


class ZabbixAPI:

    def __init__(self):
        self.url = 'http://172.16.80.130:8888/api_jsonrpc.php'
        self.header = {"Content-Type": "application/json-rpc"}

    def user_login(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "admin",
                    "password": "zabbix"
                },
                "id": 1,
                "auth": None
            }
        )

        request = urllib2.Request(self.url, data)
#        print request

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed,Please check your username and password!"
        else:
            response = json.loads(result.read())
#           print response
            result.close()

        self.auth_token = response['result']
#        print self.auth_token
        return self.auth_token

    def hosts_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": [
                        "hostid",
                        "host"
                    ],
                    "selectInterfaces": [
                        "interfaceid",
                        "ip"
                    ]
                },
                "id": 1,
                "auth": self.user_login()
            }
        )

        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
#            print result.read()
        except URLError as e:
            if hasattr(e, 'reason'):
                print e.reason
            elif hasattr(e, 'message'):
                print "Error code:", e.message
        else:
            response = json.loads(result.read())
#            print response['result']
            result.close()
        print "Number Of Hosts:", len(response['result'])
        for host in response['result']:
            print "Host ID:", host['hostid'], "Host Name:", host['host']

        print "______________________________"

    def hostgroup_get(self, groupName=''):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend",
                    "filter": {
                        "name": groupName,
                    }
                },
                "auth": self.user_login(),
                "id": 1
            }
        )

        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Info:", e.message
        else:
            response = json.loads(result.read())
#            print response
            result.close()
        print "Number Of Group:", len(response['result'])
        self.G_list = []
#        print type(G_list)
        try:
            for group in response['result']:
                # print "Group ID:", group['groupid'], "Group Name:",
                # group['name']
                print group['name']

                N = group['name']
                f = N.encode('utf-8')
#                print type(f)
                self.G_list.append(f)
#                print "G_list:", G
        except AttributeError as e:
            print "ERROR:", e.message
        print "G_list:", self.G_list

        print "_____________________________________"

    def template_get(self, templateName=''):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                    "output": "extend",
                    "filter": {
                        "name": templateName}
                },
                "auth": self.user_login(),
                "id": 1,
            }
        )

        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
#        print response
        result.close()
        print "Module_List:"
        for temp in response['result']:
            print temp['name']

        print "_______________________________"

    def create_group(self, groupName):
        if groupName in self.G_list:
            print "EXIST!"
            sys.exit(1)
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.create",
                "params": {
                    "name": groupName
                },
                "auth": self.user_login(),
                "id": 1
            }
        )

        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])
        try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        print response


a = ZabbixAPI()
a.user_login()
a.hosts_get()
a.hostgroup_get()
a.template_get()
a.create_group('Tes Servers')
