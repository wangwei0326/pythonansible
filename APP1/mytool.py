#-*- coding:UTF-8 -*-
import os,sys
import ansible.runner
reload(sys)
sys.setdefaultencoding('utf8')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class UpLoad:
    def __init__(self):
        self.uploadpath=os.path.join(BASE_DIR, 'upload')
    def uploadfile(self,filename,filecontext):
        filepath=os.path.join(self.uploadpath,filename)
        of=open(filepath,"wb")
        of.write(filecontext)
        of.closed
    def writefile(self,filepath,filecontext):
        of=open(filepath,"wb")
        of.write(filecontext)
        of.closed
    def readfile(self,filepath):
        of=open(filepath,"r+")
        file_context=of.read()
        of.closed
        return file_context
    def add_config_file(self,config_file_name,config_file_content,group_name):
        dirpath=os.path.join(self.uploadpath,group_name)
        filepath=os.path.join(dirpath,config_file_name)
        if os.path.exists(dirpath):
            if os.path.exists(os.path.join(dirpath,config_file_name)):
                self.writefile(filepath,config_file_content)
                return 1
            else:
                self.writefile(filepath,config_file_content)
                return "%s %s 添加成功" %(group_name,config_file_name)
        else:
            os.mkdir(dirpath)
            self.writefile(filepath,config_file_content)
            return "%s %s 添加成功" %(group_name,config_file_name)
    def config_file_list(self):
        group_list={}
        dirpath=os.path.join(self.uploadpath)
        for root,dirs,files in os.walk(dirpath,topdown=False):
            group_list[os.path.split(root)[1]]=files
        return group_list
    def read_config_file(self,config_file_name,group_name):
        filepath=os.path.join(self.uploadpath,group_name,config_file_name)
        file_context=self.readfile(filepath)
        return file_context
class myansible:
    def __init__(self,remote_port):
        self.remote_port=remote_port
	self.host_list='/pythonansible/hostmessage.py'
        self.private_key_file='/root/.ssh/id_rsa'
        self.forks=10
    def ansible_group(self,group,module_name,module_args):
        results = ansible.runner.Runner(
            host_list=self.host_list,
            private_key_file=self.private_key_file,
            forks=self.forks,
            remote_port=self.remote_port,
            pattern='%s*' %(group),
            module_name=module_name,
            module_args=module_args
        ).run()
        if results is None:
            print "No hosts found"
            sys.exit()
        for (hostname,result) in results['contacted'].items():
            print "%s >>> %s" %(hostname,result['stdout'])
if __name__=="__main__":
    # upload = UpLoad()
    # upload.uploadfile("abc.txt","11111")
    myansible=myansible(22)
    myansible.ansible_group('web2','command','uptime')
