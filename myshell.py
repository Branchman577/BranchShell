import os
import socket
import sys
import readline
import getpass
import mycommands as mc
import subprocess

start_dir = os.getcwd()

# reads a single line of input
def reader(Username,machinename,currentdir):
        line = input(Username + "@" + machinename + ":~"+ currentdir + " --> ").strip()
        return line

# split the input by using split
def splitter(line):
        args = line.split()
        return args

#executes the input using subprocesses to get the output needed
def runner(args):
    #checks if the process needs background execution
    if args[-1] == "&":
        subprocess.Popen(args[:-1])
    # checks if the file needs output to a file
    if args[-1] == ">":
        p = subprocess.check_output(args)
        l = p.decode('ascii').split("\n")
        return l
    # if neither is neeeded run as a normal subprocess
    else:
        p = subprocess.check_output(args)
        l = p.decode('ascii').split("\n")
        for i in l:
            print(i)

# runs the commands given as input and decies if i/o redirection or background inputs are needed
def comms(args):
        commandlist = ["cd","clr","dir","environ","echo","help","pause"]
        commandlist2 = [mc.cd,mc.clr,mc.dir,mc.env,mc.echo,mc.help,mc.pause]
        # Trys to execure one of the commands in the command list
        try:
                # check if the process needs to  be done in the background 
                if args[-1] =="&":
                    if args[0] in commandlist:
                        args = args[:-1]
                        if len(args) > 1 or args[0] == "cd" :
                                    pos = commandlist.index(args[0])

                                    #gets the actual codde needed to run the command and runs it
                                    p = subprocess.call(commandlist2[pos](" ".join(args[1:])))
                        # if the command takes no arguments do this instead
                        else:
                                #gets the actual codde needed to run the command and runs it
                                pos = commandlist.index(args[0])
                                p = subprocess.call(commandlist2[pos]())
                    else:
                        runner(args)

                # to check if check if output to a file is needed with appending
                elif ">>" in args:
                    output2(args)
                    return
                # to check if check if output to a file is needed without appending
                elif ">" in args:
                    output1(args)
                    return
                elif len(args) == 0:
                        pass # ie Pressing enter

                elif args[0] == "quit":
                        #quits out of the shell
                        quit()

                #checks if the argument is a shell specific command
                elif args[0] in commandlist :

                        #checks if the command takes arguments
                        if len(args) > 1 or args[0] == "cd" :
                                pos = commandlist.index(args[0])

                                #gets the actual codde needed to run the command and runs it
                                commandlist2[pos](" ".join(args[1:]))
                        # if the command takes no arguments do this instead
                        else:
                                #gets the actual codde needed to run the command and runs it
                                pos = commandlist.index(args[0])
                                commandlist2[pos]()
                else:
                        runner(args)

        except:
                print("")

# deals with pushing output to a file without appending to the file
def output1(args):
    commandlist = ["cd","clr","dir","environ","echo","help","pause"]
    commandlist2 = [mc.cd,mc.clr,mc.dir,mc.env,mc.echo,mc.help,mc.pause]
    # gets the index of the > in the args list
    poss = args.index(">")
    # gets the file thats output needs to go to
    outfile = poss + 1
    com = args[:outfile]
    #opens the file that output goes to
    with open(args[outfile],"w") as f:
        if args[0] in commandlist :
                        #checks if the command takes arguments
                        if len(com) > 1 or args[0] == "cd" :
                                pos = commandlist.index(args[0])

                                #gets the actual code needed to run the command and runs it
                                x = commandlist2[pos](" ".join(com[1:]))
                                #writes the list of output to the file
                                for i in x:
                                    f.write(i + "\n")
         # if the process isnt an in built process do this 
        else:
            x = runner(com)
            for i in x:
                f.write(i + "\n")

# deals with pushing output to a file while also appending to the file          
def output2(args):
    commandlist = ["cd","clr","dir","environ","echo","help","pause"]
    commandlist2 = [mc.cd,mc.clr,mc.dir,mc.env,mc.echo,mc.help,mc.pause]
    # gets the index of the >> in the args list
    poss = args.index(">>")
    # gets the file thats output needs to go to
    outfile = poss + 1
    com = args[:poss]
    com.append(">")
    #opens the file that output goes to
    with open(args[outfile],"a") as f:
        if args[0] in commandlist :
                        #checks if the command takes arguments
                        if len(com) > 1 or args[0] == "cd" :
                                pos = commandlist.index(args[0])

                                #gets the actual codde needed to run the command and runs it
                                x = commandlist2[pos](" ".join(com[1:]))
                                #writes the list of output to the file
                                for i in x:
                                    f.write(i + "\n")
        # if the process isnt an in built process do this 
        else:
            x = runner(com)
            for i in x:
                f.write(i + "\n")


# deals with taking batchfile input
def batch(args):
            try:
                # opens the file and reads the commands and executes them and quits after
                for line in open(args, "r"):
                        comms(line.split())
                quit()
            except(IndexError):
                print("BranchShell: was not able to access " + args + ": No such file or directory exists")

def main():
        print("Welcome to BranchShell! Type help to read the help file!")
        # gets the user's name, the machine's name and their current working directory
        shell = os.getcwd() + "/" + sys.argv[0]
        # check if batchfile input is being given
        if len(sys.argv) > 1:
                batch(sys.argv[1])
        else:
                # The loop of the shell
                x = True
                while x == True:
                        try:
                                Username = getpass.getuser()
                                machinename = socket.gethostname()
                                currentdir = os.getcwd()
                                currentline = reader(Username,machinename,currentdir)
                                args = splitter(currentline)
                                proid = comms(args)
                        except ValueError:
                                return

# quits out of the shell
def quit():
        print("Exiting..")
        exit()

if __name__ == "__main__":
        main()
