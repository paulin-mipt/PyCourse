import os
import shutil

def usage():
    print("### Hi, %username%. Paulin FManager v.0.9 supports the following commands:")
    print("remove <src>")
    print("mkdir <src>")
    print("copy <src> <dest>")
    print("move <src> <dest>")
    print("exit")
    print("### Now you can start working. Good luck!")
    
def exitmgr(l = ()):
    print("### Great work! Wanna see you again :)")
    exit(0)
 
def cp(l):
    src = os.path.join(os.getcwd(), l[1])
    dest = os.path.join(os.getcwd(), l[2])
    if (os.path.exists(src)):
        if (not os.path.exists(dest)):
            if (os.path.isdir(src)):
                shutil.copytree(src, dest, True)
            else:
                shutil.copyfile(src, dest)
        else:
            print("ERR: " + dest + ": already exists")
    else:
        print("ERR: " + src + ": not exists")
    
def mv(l):
    src = os.path.join(os.getcwd(), l[1])
    dest = os.path.join(os.getcwd(), l[2])
    if (os.path.exists(src)):
        if (not os.path.exists(dest)):
            shutil.move(src, dest)
        else:
            print("ERR: " + dest + ": already exists")
    else:
        print("ERR: " + src + ": not exists")
    
def rem(l):
    src = os.path.join(os.getcwd(), l[1])
    if (os.path.exists(src)):
        if (os.path.isdir(src)):
            os.removedirs(src)
        else:
            os.remove(src)
    else:
        print("ERR: " + src + ": not exists")
    
def creat(l):
    src = os.path.join(os.getcwd(), l[1])
    if (not os.path.exists(src)):
        os.makedirs(src)
    else:
        print("ERR: " + src + ": already exists")
        
cmd = {"copy" : cp, "move" : mv, "exit" : exitmgr, "mkdir" : creat, "remove" : rem}

while (1):
    cmdline = input(os.getcwd() + "$ ").split(None, 2)
    if (len(cmdline) == 0):
        usage()
    else:
        if (not cmdline[0] in cmd):
            print(cmdline[0] + ": wrong command")
        else:
            cmd[cmdline[0]](cmdline)
    
    