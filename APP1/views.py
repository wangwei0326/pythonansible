# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
import json
from APP1.models  import *
from mytool import UpLoad
import sys
import APP1.views
# 登录
def login(request):
    return render(request, 'login.html')
# 主页
def index(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.filter(user_name=username).values()
        if len(user) > 0 :
            if user[0]['user_passwd'] == password:
                request.session['id']=user[0]['user_id']
                return render(request, 'index.html',context=({'username':username}))
    return render(request,'login.html',context=({'error':'用户名或密码错误'}))

# 退出登录
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request,'login.html')

# 添加主机
def addhost(request):
    if request.session.get('id'):
        if not request.method == 'POST':
            return render(request,'addhost.html')
        else:
            hostname=request.POST['hostname'].strip()
            hostip=request.POST['hostip'].strip()
            group_name=request.POST['group_name'].strip()
            group_name_sub=request.POST['group_name_sub'].strip()
            P=Host(hostname=hostname,hostip=hostip,group_name=group_name,group_name_sub=group_name_sub)
            P.save()
        return render(request,'addhost.html',context=({'sucess':'主机添加OK'}))
    else:
        return render(request, 'login.html')

# 显示主机列表
def listhost(request):
    if request.session.get('id'):
        if request.method == 'POST':
            if request.POST['seachcontent'].strip() == '':
                hostlist=Host.objects.all().values()
                return render(request,'hostlist.html',context=({'hostlist':hostlist}))
            if request.POST['seachtype'] == 'hostip':
                seachcontent=request.POST['seachcontent']
                hostlist=Host.objects.filter(hostip=seachcontent).values()
                return render(request,'hostlist.html',context=({'hostlist':hostlist}))
            elif request.POST['seachtype']=='hostname':
                seachcontent=request.POST['seachcontent']
                hostlist=Host.objects.filter(hostname=seachcontent).values()
                return render(request,'hostlist.html',context=({'hostlist':hostlist}))
            elif request.POST['seachtype']=='group_name':
                seachcontent=request.POST['seachcontent']
                hostlist=Host.objects.filter(group_name=seachcontent).values()
                return render(request,'hostlist.html',context=({'hostlist':hostlist}))
        hostlist=Host.objects.all().values()
        return render(request,'hostlist.html',context=({'hostlist':hostlist}))
    else:
        return render(request, 'login.html')

# 删除主机
def deletehost(request):
    if request.session.get('id'):
        if request.method == 'POST':
            for k,v in request.POST.items():
                hostip=Host.objects.get(hostip=v)
                data=hostip.delete()
            return HttpResponse(data)
    else:
        return render(request, 'login.html')

# 上传文件
def upload(request):
    if request.session.get('id'):
        if not request.method == 'POST':
            return render(request,'upload.html')
        else:
            filename=request.POST['name']
            filecontext=request.FILES.get('file').read()
            upload=UpLoad()
            upload.uploadfile(filename,filecontext)
        return render(request,'upload.html',context=({'sucess':'上传OK'}))
    else:
        return render(request, 'login.html')
# 添加分组
def addgroup(request):
    if request.session.get('id'):
        if not request.method == 'POST':
            return render(request,'addgroup.html')
        else:
            group_name=request.POST['groupname']
            P=ServerGroup(group_name=group_name)
            P.save()
            return render(request,'addgroup.html',context=({'sucess':'分组添加OK'}))
    else:
        return render(request, 'login.html')

# 显示分组列表

def listgroup(request):
    if request.session.get('id'):
        grouplist=ServerGroup.objects.all().values()
        dict_group={}
        for i in grouplist:
            dict_group[i['group_name']]={'group_name_sub':i['group_name_sub'].split()}
        if request.method == 'POST':
            if request.POST.has_key('seachcontent'):
                if not request.POST['seachcontent'].strip() == '':
                    dict_group1={}
                    dict_group1[request.POST['seachcontent']]=dict_group[request.POST['seachcontent']]
                    return render(request,'grouplist.html',context=({'grouplist':dict_group1}))
                return render(request,'grouplist.html',context=({'grouplist':dict_group}))
            return HttpResponse(json.dumps(dict_group))
        return render(request,'grouplist.html',context=({'grouplist':dict_group}))
    else:
        return render(request,'login.html')
# 添加子分组
def add_sub_group(request):
    if request.session.get('id'):
        if not request.method == 'POST':
            return HttpResponseRedirect('/listgroup/')
        else:
            group_name=request.POST['inputgroupname']
            group_name_sub=request.POST['inputsubgroupname']
            P=ServerGroup.objects.get(group_name=group_name)
            if P.group_name_sub == None :
                P.group_name_sub=group_name_sub
            else:
                P.group_name_sub= P.group_name_sub + '  '+ group_name_sub
            P.save()
            return redirect(reverse(APP1.views.listgroup))
    else:
        return redirect(reverse(APP1.views.login))
def add_config_file(request):
    if request.session.get('id'):
        if not request.method == 'POST':
            return render(request,'configuration_file.html')
        else:
            config_file_name=request.POST['config_file_name']
            config_file_content=request.POST['config_file_content']
            group_name=request.POST['group_name']
            if (config_file_name.strip()  or config_file_content.strip()) == '':
                return render(request,'configuration_file.html',context=({"sucess":"文件名或内容为空"}))
            else:
                upload=UpLoad()
                result=upload.add_config_file(config_file_name,config_file_content,group_name)
                if result==1:
                    grouplist=upload.config_file_list()
                    return render(request,'config_file_list.html',context=({"sucess":"文件更新OK",'grouplist':grouplist}))
                return render(request,'configuration_file.html',context=({"sucess":"%s" %(result)}))
    return redirect(reverse(APP1.views.login))

def list_config_file(request):
    if request.session.get('id'):
        grouplist1={}
        upload=UpLoad()
        grouplist=upload.config_file_list()
        if not request.method == 'POST' or request.POST['seachcontent'].strip() == '' :
            return render(request,'config_file_list.html',context=({'grouplist':grouplist}))
        else:
            grouplist1[request.POST['seachcontent']]=grouplist[request.POST['seachcontent']]
            return render(request,'config_file_list.html',context=({'grouplist':grouplist1}))
    return redirect(reverse(APP1.views.login))
def read_config_file(request):
    if request.session.get('id'):
        config_file_name=request.POST['config_file_name']
        group_name=request.POST['group_name']
        upload=UpLoad()
        config_file_context=upload.read_config_file(config_file_name,group_name)
        return HttpResponse(config_file_context)
    return redirect(reverse(APP1.views.login))
