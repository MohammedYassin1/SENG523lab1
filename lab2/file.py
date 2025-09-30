# def myfunction(a, b):
#     secret_var = "HEYTHERE"

# def myfunction(a, b):
#     var = "WOWSECRET_12_ABCD"

# def myfunction(a, b):
#     mytoken = "WOWSECRET_4242_AAAA"

# def myfunction(a, b):
#     myvar = "HULLO"

import os

# def myfunction(a, b):
#     cmd = input()
#     a = cmd + cmd
#     print(a)

# def myfunction(a, b):
#     var = "cat meow.txt"
#     os.system(var)

def myfunction(a, b):
    cmd = input()
    cmd2 = "ls –l " + cmd
    cmd3 = remove_spaces(cmd2)
    os.system(cmd3)

# def myfunction(a, b):
#     cmd = input()
#     cmd2 = "ls –l " + cmd
#     cmd3 = sanitized(cmd2)
#     os.system(cmd3)