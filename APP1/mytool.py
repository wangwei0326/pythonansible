#-*- coding:UTF-8 -*-
import os,sys
import ansible.runner
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class UpLoad:
    def __init__(self):
        self.uploadpath=os.path.join(BASE_DIR, 'upload')
    def uploadfile(self,filename,filecontext):
        filepath=os.path.join(self.uploadpath,filename)
        of=open(filepath,"wb")
        of.write(filecontext)
        of.closed
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
