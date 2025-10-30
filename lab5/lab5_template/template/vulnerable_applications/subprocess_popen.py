import subprocess

def popen1(user):
    subprocess.Popen("echo " + user)

def popen2(user):
    subprocess.Popen("echo " + user, shell=True)

def popen3(user):
    subprocess.run(["sh", "-c", "echo " + user])

def popen4(user):
    subprocess.run(["sh", "-c", "echo " + user], shell=True)

def popen5(user):
    subprocess.Popen("echo hello", shell=True)

def popen6():
    subprocess.run(["echo", "hello"], shell=True)
