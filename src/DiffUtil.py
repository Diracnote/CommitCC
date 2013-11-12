'''
Created on 2013-11-12 11:06

@author: Diracnote
'''
import subprocess
import sys

class DiffUtil(object):
    '''
    classdocs
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
            self.new = []
            self.mod = []
            self.gone = []
            for line in lines:
                outLine = line.decode(sys.getdefaultencoding())
                preMod = "Files"
                if outLine.startswith(preMod):
                    midMod = "and"
                    sufMod = "differ"
                    localPath = outLine[len(preMod):outLine.find(midMod)].strip()
                    remotePath = outLine[outLine.find(midMod) + len(midMod):outLine.find(sufMod)].strip()
                    self.mod.append((localPath, remotePath))
                    print(self.mod)
                    
if __name__ == '__main__':
    localRepo = r"C:\Demo\brt"
    remoteRepo = r"E:\CNCC_DEV\ClearCaseWork\feichen_PRO_PISA_DEV\VC_PISA\PISA_SRC\BRTS\brts"
    # cmd = " ".join(["diff", diffArgs, localRepo, ccRepo])
    # pipe = subprocess.Popen(cmd)
    diff = DiffUtil(localRepo, remoteRepo)

