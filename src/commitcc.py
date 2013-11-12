'''
Created on 2013-11-12 00:14

@author: Diracnote
'''
import subprocess
import sys

if __name__ == '__main__':
    diffArgs = "--brief"
    localRepo = r"C:\Demo\brt"
    ccRepo = r"E:\CNCC_DEV\ClearCaseWork\feichen_PRO_PISA_DEV\VC_PISA\PISA_SRC\BRTS\brts"
#     cmd = " ".join(["diff", diffArgs, localRepo, ccRepo])
#     pipe = subprocess.Popen(cmd)
    rc = subprocess.Popen(["diff", diffArgs, localRepo, ccRepo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if rc == None:
        print("There were some errors")
    
#     line = rc.stdout.readline()
#     out = line.decode(sys.getdefaultencoding())
    lines = rc.stdout.readlines()
    for line in lines:
        out = line.decode(sys.getdefaultencoding())
        print(out, end="")
