import os

def constantstr():
    os.system("echo hello")  

def variable1(cmd):
    os.system(cmd)  

def variable2(user):
    os.system("ls " + user)  

def variable3(user):
    os.system(f"echo {user}")

