#!/usr/bin/env python
#coding:utf8
import json
import sys
def group():
    info_dict = {"all":["10.0.91.250","127.0.0.1"]}
    print json.dumps(info_dict,indent=4)
def host(ip):
    info_dict = {"10.0.91.250":{"host":"10.0.91.250"},"127.0.0.1":{"host":"127.0.0.1"}}
    print json.dumps(info_dict[ip],indent=4)
if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    group()
elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    host(sys.argv[2])
else:
    print "Usage: %s --list or --host <hostname>" % sys.argv[0]
    sys.exit(1)
