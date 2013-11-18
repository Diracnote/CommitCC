# encoding: utf-8
'''
Created on 2013-11-12 11:06

@author: Diracnote
'''
import subprocess
import sys
import os
import configparser

class DiffUtil(object):
    '''
    对传入的目录进行对比，并解析结果，分别以元组的形式存入列表中
    结果列表：
        相同的目录：comm
        修改文件：mod
        新加文件：new
        删除文件：gone
    '''
    
    def __init__(self, localRepo, remoteRepo, command="diff", args=["--brief", "-r"], ignore_file="config.ini"):
        '''
        Constructor
        '''
        self.localRepo = localRepo
        self.remoteRepo = remoteRepo
        self.command = command
        args = self.initIgnore(args, ignore_file)
        self.args = args
        
        self.comm = []
        self.mod = []
        self.new = []
        self.gone = []
        commandlist = ["diff"] + [self.localRepo, self.remoteRepo] + list(args)
        print("Diff命令：" + " ".join(commandlist))
        print("=" * 20)
        print("Wait for diff ...")
        rc = subprocess.Popen(commandlist, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if rc == None:
            print("Diff Command Error!")
            print("=" * 20)
            return None
        else:
            lines = rc.stdout.readlines()
            print("Diff done!")
            print("=" * 20)
            for line in lines:
#                 outLine = line.decode(sys.getdefaultencoding())
                outLine = line.decode("GBK")  # 此处中文环境Windows命令行输出编码为GBK
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
        
    def initIgnore(self, args, config_file):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(config_file)
        if "PATTERN" not in config["IGNORE"]:
            print("CONFIG文件[IGNORE]段无PATTERN键")
            sys.exit(0)
        pattern_str = config.get("IGNORE", "PATTERN")
#         if pattern == "":
#             return args
        pattern_list = pattern_str.split(" ")
        print("忽略文件模式列表：")
        for ignore in pattern_list:
            if ignore != "":
                print(ignore)
                args.extend(["-x", ignore])
        return args
