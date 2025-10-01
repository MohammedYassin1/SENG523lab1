# def myfunction(a, b):
#     c = a + 20 - b # <-- c is defined,
#     d = a # but never used
#     e = b
#     return d, e

# def outiefunc (a, b):
#     c = 30 # <--c is defined, but not used
#     d = a + b
#     def inniefunc(x, y):
#         c = 15 # <--this is a different c!
#         return c
#     return d

# def outiefunc (a, b):
#     c = 30 # <-- c is defined here...
#     d = a + b
#     def inniefunc(x, y):
#         retval = c*2 # <-- ...and used here
#         return retval
#     return d

# def myfunction(a, b):
#     x = 20 # <-- outer x
#     def myotherfunction():
#         x = 10 # <-- inner x shadows outer x

# def myfunction(a, b):
#     c = a + b
#     d = b + c
#     return d

# def myfunction(a, b):
#     c = a * b
#     if c != 0:
#         print("Nonzero")
#         return 0
#     else:
#         print("Zero")
#         return c
    
# def myfunction(a, b):
#     if a != b:
#         c = a-b
#         return c
#     else:
#         c = 0

# def myfunction(a, b):
#     if a != b:
#         c = a-b
#         return c
#         print("Different")
#     else:
#         return 0

# def myfunction(a, b):
#     if a != 0:
#         print("Nonzero")

# def myfunction(a, b):
#     if a:
#         print("a")

# def myfunction(a, b):
#     if "hello":
#         print("Hello")

# def myfunction(a, b):
#     if 0 == a:
#         print("Yep, still zero")

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

# def myfunction(a, b):
#     cmd = input()
#     cmd2 = "ls –l " + cmd
#     cmd3 = remove_spaces(cmd2)
#     os.system(cmd3)

# def myfunction(a, b):
#     cmd = input()
#     cmd2 = "ls –l " + cmd
#     cmd3 = sanitized(cmd2)
#     os.system(cmd3)