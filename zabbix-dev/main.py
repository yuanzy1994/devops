#-*-coding:utf-8-*-

import json
import urllib2
from urllib2 import URLError
import sys


class ZabbixAPI:
    G_list = []
    GID_list = []
    G_dic = {}
    GID = None

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
            print response['result']
            result.close()
        #print "Number Of Hosts:", len(response['result'])
        for host in response['result']:
            print "Host ID:", host['hostid'], "Host Name:", host['host']

        print "______________________________"

    def hostgroup_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend",
                    "filter": {
                        "name": sys.argv[3],
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
        #print "Number Of Group:", len(response['result'])
#        print type(G_list)
        try:
            for group in response['result']:

        #        print "Group ID:", group['groupid'], "Group Name:",group['name']
                self.G_dic[group['name'].encode('utf-8')] = int(group['groupid'].encode('utf-8'))
                self.GID_list.append(group['groupid'].encode('utf-8'))
                self.G_list.append(group['name'].encode('utf-8'))
                self.GID=int(group['groupid'].encode('utf-8'))
        except AttributeError as e:
            print "ERROR:", e.message
#        print "G_list:", self.G_list
#        print "Gid_list",self.GID_list

        return self.GID


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
        print response
        result.close()
        print "Module_List:"
        for temp in response['result']:
            print temp['name'], temp['templateid']

        print "_______________________________"

    def create_group(self,groupName=sys.argv[3]):
        self.hostgroup_get()
#        print self.G_list
        if groupName in self.G_list:
#           sys.exit(1)
            return self.hostgroup_get()
        else:
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

            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            return self.hostgroup_get()
    #        print "hello:", response

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

    def host_create(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": {
                    "host": sys.argv[1],
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": sys.argv[2],
                            "dns": "",
                            "port": "10050"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": self.create_group(sys.argv[3])
                        }
                    ],
                    "templates": [
                        {
                            "templateid": "10001"
                        }
                    ],
                    "inventory_mode": 0,
                    "inventory": {
                        "macaddress_a": None,
                        "macaddress_b": None,
                    }
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
        print response
        print "host create success!"
#        print self.create_group(sys.argv[3])


a = ZabbixAPI()
a.user_login()
# a.hosts_get()
#a.hostgroup_get()
#a.template_get()
#a.create_group('Dev Server')
#
# a.host_create('jenkins', '192.168.2.108')
# a.host_create('dev-basic', '192.168.2.38')
# a.host_create('dev-nginx', '172.16.80.20')
a.host_create()
