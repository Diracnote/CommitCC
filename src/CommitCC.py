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
import configparser
from os import sep
import os

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
            print(" ".join(["NEW:", sep.join(line)]))
            self.__commitNew(line)
        for line in diff.gone:
            print(" ".join(["GONE:", sep.join(line)]))
            self.__commitDel(line)
        for line in diff.mod:
            print(" ".join(["MOD:", str(line)]))
            self.__commitMod(line)
            
    def __commitNew(self, rc=("", "")):
        localfile = sep.join(rc)
        relpath = os.path.relpath(localfile, self.local)
        remotefile = "/".join([self.remote, relpath])
        # 在CC上创建文件父目录
        remote_dir = dirname(remotefile)
        while not isdir(remote_dir):
            middir = remote_dir
            while not isdir(dirname(middir)):
                middir = dirname(middir)
            mkdir(middir)
            self.cc.checkout(dirname(middir))
            self.cc.mkdir(middir)
            self.cc.checkin(dirname(middir))
        if self.cc.checkout(dirname(remotefile)) == 0:
            copyfile(localfile, remotefile)
            self.cc.mkelem(remotefile)
        self.cc.checkin(dirname(remotefile))
    
    def __commitDel(self, rc=("", "")):
        path = rc[0]
        file = sep.join(rc)
        self.cc.checkout(path)
        self.cc.rm(file)
        self.cc.checkin(path)
    
    def __commitMod(self, rc=("", "")):
        local_file, remote_file = rc
        if self.cc.checkout(remote_file) == 0:
            copyfile(local_file, remote_file)
        self.cc.checkin(remote_file)
    
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.optionxform = str
    config_file = "config.ini"
    config.read(config_file)
    local = config.get("REPO", "LOCAL")
    remote = config.get("REPO", "CC")
    print("".join(["本地代码：", local]))
    print("".join(["CC代码：", remote]))
    cc = CommitCC()
    cc.commit(local, remote)
