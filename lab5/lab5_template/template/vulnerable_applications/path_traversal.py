import os

def opener(user):
    f = open(user)
    f.close()

def opener_concat(user):
    f = open("uploads/" + user) 
    f.close()

def opener_const_concat():
    f = open("uploads/" + "userfiles") 
    f.close()

def opener_join_var(base, name):
    p = os.path.join(base, name) 
    return open(p)

def opener_join_varconst(base):
    p = os.path.join(base, "downloads") 
    return open(p)

def opener_join_const(base, name):
    p = os.path.join("home", "myfiles") 
    return open(p)
