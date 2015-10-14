"""creating a simple shell my self
   tested using flake8""" 


import os
import sys

def print_err(error_msg):
    print error_msg
    sys.exit(1)

def getLine(list1, list2, list3, pipe1 = False, pipe2 = False, 
            toBackground = False, redirection = False, 
            redirectedFile = ['']):
    fd = sys.stdin
    len1 = 0
    print '>>>',
    while True:
        line = fd.read(1)
        if line != '\n' and line != '&' \
            and line != '>' and line != '|' and line != '':
            list1[0] += line
        else:
            break
        len1 += 1
    if len1 == 0 and line == '':
        return None
    if line == '&':
        toBackground = True
    if line == '>':
        redirection = True
        line = fd.read(1)
        while line.isspace():
            line = fd.read(1)
        while line.isalnum():
            redirectedFile[0] += line
            line = fd.read(1)
       # print redirectedFile
    if line == '|':
        pipe1 = True
        len2 = 0
        while True:
            line = fd.read(1)
            if line != '\n' and line != '' and line != '|':
                list2[0] += line
            else:
                break
           # len2 += 1
        if len2 == 0 and line == '':
            print_err("nothing after '|'")
        if line == '|':
            pipe2 = True
            len2 = 0
            while True:
                line = fd.read(1)
                if line != '\n' and line != '':
                    list3[0] += line
                else:
                    break
                if len2 == 0 and line == '':
                    print_err("nothing after '|'") 
    return pipe1, pipe2, toBackground, redirection, redirectedFile

def main():
    """ define the main function """
    argc = len(sys.argv)
    if argc > 1 or (argc > 1 and sys.argv[1] == "help" ):
        print_err("%s- a simple shell interpreter,no arg needed"%sys.argv[0])
    
    pipe1 = toBackground = redirection = redirectedFile = None
    while True:
        list1 = ['']
        list2 = ['']
        list3 = ['']
        res = getLine(list1, list2, list3)
        if res == None:
            break

        pipe1, pipe2, toBackground, redirection, redirectedFile = res
        argv1 = list1[0].split()
        argv2 = list2[0].split()
        argv3 = list3[0].split()
        pfd1 = os.pipe()
        pfd2 = os.pipe()
        if argv1 == []:
            continue

        child = os.fork()
        if child == -1:
            print_err("fork-error occured")

        elif child == 0:
            if pipe1:
                os.close(pfd1[0])
                os.close(pfd2[0])
                os.close(pfd2[1])
                if pfd1[1] != sys.stdout.fileno():
                    os.dup2(pfd1[1], sys.stdout.fileno())
                    os.close(pfd1[1])
            if redirection:
                fd = open(redirectedFile[0], 'w')
                if fd != 1:
                    os.dup2(fd.fileno(), 1)
            try:
                os.execlp(argv1[0], *argv1)
            except OSError:
                print "%s--> command not found" %argv1[0]
            else:
                print_err("execlp-error occured")

        else:
            if not pipe1 and not toBackground:
                os.wait()

        if pipe1:
            child = os.fork()
            if child == -1:
                print_err('fork-error occured')

            elif child == 0:
                os.close(pfd1[1])
                os.close(pfd2[0]) 
                if pfd1[0] != sys.stdin.fileno():
                    os.dup2(pfd1[0], sys.stdin.fileno())
                    os.close(pfd1[0])

                if pipe2:
                    if pfd2[1] != sys.stdout.fileno():
                        os.dup2(pfd2[1], sys.stdout.fileno())
                        os.close(pfd2[1])

                else:
                    os.close(pfd2[1])

                try:
                    os.execlp(argv2[0], *argv2)
                
                except OSError:
                    print "%s--> command not found" %argv2[0]

                else:
                    print_err('execlp-error occured')

        if pipe2:
            child = os.fork
            if child == -1:
                print_err('fork-error occured')
            elif child == 0:
                os.close(pfd2[1])
                os.close(pfd1[0])
                os.close(pfd1[1])
                if pfd2[0] != sys.stdin.fileno():
                    os.dup2(pfd2[0], sys.stdin.fileno())
                    os.close(pfd2[0])

                try:
                    os.execlp(argv3[0], *argv3)
                except OSError:
                    print "%s-->command not found" %argv3[0]
                else:
                    print_err('execlp-error occured')
        os.close(pfd1[0])
        os.close(pfd1[1])
        os.close(pfd2[0])
        os.close(pfd2[1])
        if pipe1:
            os.wait()
            os.wait()
        if pipe2:
            os.wait()

        pipe1 = False
        pipe2 = False
        toBackground = False
        redirection = False

    print

main()
