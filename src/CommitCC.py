# encoding: utf-8
'''
Created on 2013-11-12 00:14

@author: DiracNote
'''

from ClearCaseConnecter import ClearCase
from DiffUtil import DiffUtil
from shutil import copyfile
from os.path import dirname
from os.path import isdir
from os.path import relpath
from os import mkdir

class CommitCC(object):
    '''
    
    '''

    def __init__(self):
        self.cc = ClearCase()
        
    def commit(self, local, remote):
        diff = DiffUtil(local, remote)
        self.local = local
        self.remote = remote
        for line in diff.new:
            print(" ".join(["NEW:", "/".join(str(line))]))
            self.__commitNew(line)
        for line in diff.gone:
            print(" ".join(["GONE:", "/".join(str(line))]))
            self.__commitDel(line)
        for line in diff.mod:
            print(" ".join(["MOD:", str(line)]))
            self.__commitMod(line)
            
    def __commitNew(self, rc=("", "")):
        relpath = relpath("/".join(rc), self.local)
        remote_file = "/".join([self.remote, relpath])
        # 在CC上创建文件父目录
        remote_dir = dirname(remote_file)
        while not isdir(remote_dir):
            mid_dir = remote_dir
            while not isdir(dirname(mid_dir)):
                mid_dir = dirname(mid_dir)
            mkdir(mid_dir)
            self.cc.checkout(dirname(mid_dir))
            self.cc.mkdir(mid_dir)
            self.cc.checkin(dirname(mid_dir))
        self.cc.checkout(dirname(remote_file))
        self.cc.mkelem(remote_file)
        self.cc.checkin(dirname(remote_file))
    
    def __commitDel(self, rc=("", "")):
        path = rc[0]
        file = "/".join(rc)
        self.cc.checkout(path)
        self.cc.rm(file)
        self.cc.checkin(dir)
    
    def __commitMod(self, rc=("", "")):
        local_file, remote_file = rc
        self.cc.checkout(remote_file)
        copyfile(local_file, remote_file)
        self.cc.checkin(remote_file)
    
if __name__ == "__main__":
    #TODO: 通过config处理CC提交
    pass