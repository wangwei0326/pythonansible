#!/usr/bin/env python
import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pythonansible.settings")
import django
django.setup()
from APP1.models import Host
import json
host = Host.objects.all().values()
info_dict={}
def group_info():
    info_dict['all']=[]
    for i in host:
	info_dict['all'].append(i['hostip'])
    print json.dumps(info_dict,indent=4)
def host_info(ip):
    pass
if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    group_info()
elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    host_info(sys.argv[2])
else:
    print "Usage: %s  --list or --host <hostname>" % sys.argv[0]
    sys.exit(1)
