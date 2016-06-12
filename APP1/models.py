from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    user_passwd = models.CharField(max_length=20)
    usergroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'

class Usergroup(models.Model):
    usergroup_id = models.AutoField(primary_key=True)
    usergroup_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'usergroup'

class Host(models.Model):
    hostname = models.CharField(max_length=20)
    hostip = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'host'

class ConfigFileSet(models.Model):
    hostip = models.CharField(max_length=20)
    config_file_name = models.CharField(max_length=100)
    content = models.TextField()
    version_num = models.IntegerField()
    user_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'config_file_set'
