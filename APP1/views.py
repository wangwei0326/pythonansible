# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from APP1.models  import User,Usergroup,Host
from mytool import UpLoad
# Create your views here.
def login(request):
    return render(request, 'login.html')
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
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request,'login.html')
def addhost(request):
    if request.session.get('id'):
        if len(request.POST)==0:
            return render(request,'addhost.html')
        else:
            hostname=request.POST['hostname']
            hostip=request.POST['hostip']
            P=Host(hostname=hostname,
                   hostip=hostip)
            P.save()
        return render(request,'addhost.html',context=({'sucess':'主机添加OK'}))
    else:
        return render(request, 'login.html')

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
        hostlist=Host.objects.all().values()
        return render(request,'hostlist.html',context=({'hostlist':hostlist}))
    else:
        return render(request, 'login.html')

def deletehost(request):
    if request.session.get('id'):
        if request.method == 'POST':
            for k,v in request.POST.items():
                hostip=Host.objects.get(hostip=v)
                data=hostip.delete()
            return HttpResponse(data)
    else:
        return render(request, 'login.html')

def upload(request):
    if request.session.get('id'):
        if len(request.POST)==0:
            return render(request,'upload.html')
        else:
            filename=request.POST['name']
            filecontext=request.FILES.get('file').read()
            upload=UpLoad()
            upload.uploadfile(filename,filecontext)
        return render(request,'upload.html',context=({'sucess':'上传OK'}))
    else:
        return render(request, 'login.html')