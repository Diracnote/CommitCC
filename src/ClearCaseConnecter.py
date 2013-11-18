'''
Created on 2013-11-13 12:23

@author: DiracNote
'''

# 调用CCRC命令所用
import subprocess
# 调用系统编码所用
import sys
# 设置环境变量所用
import os
# 处理ini配置文件
import configparser

class ClearCase(object):
    '''
    Clear Case直接调用模块
    
    采用单行命令调用CCRC，若与CCRC进行交互操作，可能需要pexpect，待以后试试
    '''

    def __init__(self, server="", username="", password="", config_file="config.ini"):
        '''
        构造器，初始化服务器，用户名，密码
        '''
        self.server = server
        self.username = username
        self.password = password
        self.ccrc = "rcleartool"
        self.commands = {
                       "login":"login",
                       "logout":"logout",
                       "mkelem":"mkelem",
                       "rm":"rm",
                       "checkout":"checkout",
                       "uncheckout":"uncheckout",
                       "checkin":"checkin"
        }
        self.__initConfig(config_file)
    
    def __initConfig(self, config_file="config.ini"):
        config = configparser.ConfigParser()
        config.optionxform = str
#         config.optionxform = lambda option: option
        config_file = "config.ini"
        config.read(config_file)
        if "CCRC_PATH" not in config["PATH"] or "CCRCCLI" not in config["PATH"]:
            print("CONFIG文件[PATH]段不存在")
            sys.exit(0)
        ccrcPath = config.get("PATH", "CCRC_PATH")
        ccrcCli = config.get("PATH", "CCRCCLI")
        if ccrcPath == "" or ccrcCli == "":
            print("CONFIG文件[PATH]段配置不正确")
            sys.exit(0)
        #TODO: 暂未完全判断路径不正确的常情况
        rcleartool = "/".join([ccrcCli, "rcleartool"])
        if os.path.isfile(rcleartool):
            self.ccrc = rcleartool
        else:
            print("CONFIG文件[PATH]段CCRCCLI路径配置不正确")
            sys.exit(0)
        os.putenv("CCRC_PATH", ccrcPath)
        shellPath = os.environ["PATH"]
        if ccrcCli not in shellPath:
            os.environ["PATH"] = ";".join([shellPath, ccrcCli])
        
        if "License_Accept" in config["LICENSE"]:
            ccrclicense = config.get("LICENSE", "License_Accept")
            os.putenv("License_Accept", ccrclicense)
        else:
            print("CONFIG文件[LICENSE]段不存在,请确保已接受CCRCCLI的协议！")
            
        if self.server == "":
            self.server = config.get("SERVER", "SERVER")
        if self.username == "":
            self.username = config.get("SERVER", "USERNAME")
        if self.password == "":
            self.password = config.get("SERVER", "PASSWORD")

    def login(self, filePath, args=("",)):
        command = self.__getCommand(self.commands.get("login"), args)
        return self.__excute(command, filePath)
     
    def logout(self, filePath, args=("",)):
        command = self.__getCommand(self.commands.get("logout"), args)
        return self.__excute(command, filePath)
        
    #创建元素（文件及文件夹）
    def mkelem(self, filePath, args=("-nc",)):
        command = self.__getCommand(self.commands.get("mkelem"), args)
        return self.__excute(command, filePath)
        
    #CCRCCLI无mkdir命令，故用mkelem –eltype directory代替
    def mkdir(self, filePath, args=("-nc","-eltype", "directory")):
        command = self.__getCommand(self.commands.get("mkelem"), args)
        return self.__excute(command, filePath)
    
    def rm(self, filePath, args=("-nc",)):
        command = self.__getCommand(self.commands.get("rm"), args)
        return self.__excute(command, filePath)
        
    def checkout(self, filePath, args=("-nc",)):
        command = self.__getCommand(self.commands.get("checkout"), args)
        return self.__excute(command, filePath)
    
    def uncheckout(self, filePath, args=("-keep",)):
        command = self.__getCommand(self.commands.get("uncheckout"), args)
        return self.__excute(command, filePath)
    
    def checkin(self, filePath, args=("-nc",)):
        command = self.__getCommand(self.commands.get("checkin"), args)
        return self.__excute(command, filePath)
    
    def __getCommand(self, command, args=("",)):
        return " ".join([self.ccrc, command, "-username", self.username, "-ser", self.server, "-pas", self.password] + list(args))
    
    def __excute(self, command, filePath):
        command = " ".join([command, filePath])
        print(command)
        rc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if rc == None:
            print(" ".join(["CCRC Command Error:", command]))
            return 1
             
        outinfo,errinfo = rc.communicate()
        if len(outinfo) != 0:
#             out = line.decode("UTF-8")
            out = outinfo.decode("GBK")
#             out = line.decode(sys.getdefaultencoding())
            print(out, end="")
            if(out.startswith("CRCLI1095E")):
                return 1
        else:
            out = errinfo.decode("GBK")
            if not out.startswith("环境变量"):
                print(out, end="")
        return 0
