'''
Created on 2013-11-12 11:06

@author: Diracnote
'''
import subprocess
import sys
import os

class DiffUtil(object):
    '''
    对传入的目录进行对比，并解析结果，分别以元组的形式存入列表中
    结果列表：
        相同的目录：comm
        修改文件：mod
        新加文件：new
        删除文件：gone
    '''
    
    def __init__(self, localRepo, remoteRepo, command="diff", args=("--brief",)):
        '''
        Constructor
        '''
        self.localRepo = localRepo
        self.remoteRepo = remoteRepo
        self.command = command
        self.args = args
        
        rc = subprocess.Popen(["diff", " ".join(self.args), self.localRepo, self.remoteRepo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if rc == None:
            print("Diff Command Error!")
            return None
        else:
            lines = rc.stdout.readlines()
            self.comm = []
            self.mod = []
            self.new = []
            self.gone = []
            for line in lines:
                outLine = line.decode(sys.getdefaultencoding())
                if(localRepo in outLine and remoteRepo in outLine):
                    preLocalPos = outLine.find(localRepo)
                    preRemotePos = outLine.find(remoteRepo)
                    localPath = outLine[preLocalPos:outLine.find(" ", preLocalPos + len(localRepo))].strip()
                    remotePath = outLine[preRemotePos:outLine.find(" ", preRemotePos + len(remoteRepo))].strip()
                    if(os.path.isdir(localPath)):
                        self.comm.append((localPath, remotePath))
                    else:
                        self.mod.append((localPath, remotePath))
                if(localRepo in outLine and remoteRepo not in outLine):
                    preLocalPos = outLine.find(localRepo)
                    localPath = outLine[preLocalPos:outLine.find(":", preLocalPos + len(localRepo))].strip()
                    localName = outLine[outLine.rfind(" "):].strip()
                    self.new.append((localPath, localName))
                if(localRepo not in outLine and remoteRepo in outLine):
                    preRemotePos = outLine.find(remoteRepo)
                    remotePath = outLine[preRemotePos:outLine.find(":", preRemotePos + len(remoteRepo))].strip()
                    remoteName = outLine[outLine.rfind(" "):].strip()
                    self.gone.append((remotePath, remoteName))


if __name__ == '__main__':
    localRepo = r"C:\Demo\brt"
    remoteRepo = r"E:\CNCC_DEV\ClearCaseWork\feichen_PRO_PISA_DEV\VC_PISA\PISA_SRC\BRTS\brts"
    # cmd = " ".join(["diff", diffArgs, localRepo, ccRepo])
    # pipe = subprocess.Popen(cmd)
    diff = DiffUtil(localRepo, remoteRepo)
    