"""pythonansible URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import APP1.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
url(r'^$', APP1.views.login),
    url(r'^index', APP1.views.index),
    url(r'^logout', APP1.views.logout),
    url(r'^addhost', APP1.views.addhost),
    url(r'^listhost', APP1.views.listhost),
    url(r'^deletehost', APP1.views.deletehost),
    url(r'^upload', APP1.views.upload),
    url(r'^addgroup', APP1.views.addgroup),
    url(r'^listgroup', APP1.views.listgroup),
    url(r'^add_sub_group', APP1.views.add_sub_group),
    url(r'^add_config_file', APP1.views.add_config_file),
    url(r'^list_config_file', APP1.views.list_config_file),
    url(r'^read_config_file', APP1.views.read_config_file),
]
