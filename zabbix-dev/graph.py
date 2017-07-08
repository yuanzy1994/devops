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
        for key in self.header:
            request.add_header(key, self.header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()

        self.auth_token = response['result']
        return self.auth_token

    def hosts_get(self):
        self.hostid = []
#        print type(self.hostid)
        self.hostname = []
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
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()

#        print response['result']
        for host in response['result']:
            print "Host ID:", host['hostid'], "Host Name:", host['host']
            self.hostid.append(host['hostid'].encode('utf-8'))
            self.hostname.append(host['host'].encode('utf-8'))

        # print self.hostid
        # print self.hostname

    def graph_get(self, hostID):
        self.graphid = []
        self.name = []
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.get",
                "params": {
                    "output": "extend",
                    "hostids": hostID,
                    "sortfield": "name"
                },
                "auth": self.user_login(),
                "id": 1
            }
        )

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()

#        print response
        for graph in response['result']:
            print graph['graphid']
            print graph['name']
            self.graphid.append(graph['graphid'].encode('utf-8'))
            self.name.append(graph['name'].encode('utf-8'))


object = ZabbixAPI()
object.user_login()
object.hosts_get()
object.graph_get(10105)
