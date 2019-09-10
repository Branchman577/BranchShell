import os
import sys
from os.path import expanduser
import threading
import myshell

# change directory command, changes the directory based on args provided otherwise, gives an error message
def cd(args):
        try:    
                # if  output ot a file is needed
                if args == ">":
                    args = 0
                    if args == 0:
                        x = []
                        x.append(os.getcwd())
                        x.append("\n")
                        return(x)
                if len(args) == 0:
                        print(os.getcwd())
                else:
                        return os.chdir(args)
        except Exception as e:
                print("cd: no such file or directory: " + args)

# clear command, clears the screen
def clr():
        # it clears the screen
        print("\x1b[2J\x1b[H",end="")

# dir command, lists the current diectory or if whatver driectory is given
def dir(d = 0):
        print(d)
        # if wanting to list the current directory with output to a file
        if d == ">":
            x = []
            for i in os.listdir(os.getcwd()):
                x.append(i)
            x.append("\n")   
            return x
        #if no dir is given lists the contents of the current dir
        if d == 0:
                for i in os.listdir(os.getcwd()):
                                print(i)
        #lists the contents of d the diretory given
        else:
                # if output to a file is needed
                if ">" == d[-1]:
                    x = []
                    y = d[:-1].strip()
                    for i in os.listdir(y):
                        x.append(i)
                    return x
                if os.path.isdir(d):
                        for i in os.listdir(d):
                                print(i)
                else:
                        print(d + " is not a valid directory.")
# environ command, prints all the current enviroment strings
def env(inp = 0):
         #lists all the environ strings
        en = os.environ
        #checks if output to a file is needed
        if inp == ">":
            x = []
            for i in en:
                x.append(en[i])
            x.append("\n")
            return x
        for i in en:
                print(en[i])

# echo command, echos back whatever comment is given
def echo(comment):
    c = comment.split()
    # check if output to a file is needed
    if comment[-1] == ">":
        c = comment[:-1].split()
        c =  " ".join(c)+ "\n"
        x = []
        x.append(c)
        return x
    else:
        print(" ".join(c)+ "\n")

# help command, prints out the readme file
def help(inp = 0):
        filename = myshell.start_dir + "/readme"
        if inp == ">":
            j = 0
            with open(filename, "r") as file:
                    f = file.readlines()
                    f.append("\n")
                    return f
        else:
            j = 0
            with open(filename, "r") as file:
                    f = file.readlines()
                    for i in f:
                            if j == 20:
                                    input("Press Enter to read next 20 lines:")
                                    j = 0
                            print(i.strip())
                            j = j + 1
        return
# pause the shell until enter is entered into the shell
def pause():
        threading.Lock().acquire()
        input("Press Enter to stop the pause:")
        threading.Lock().release()
        return
