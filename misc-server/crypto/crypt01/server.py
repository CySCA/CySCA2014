###################################################################################
# This file contains the implementation of the first crypto challenge for CySCA2014
###################################################################################
import socket
import random
import subprocess
import os
import signal
import helpers

def shuffle_plain(plain):
    plain = list(plain)
    random.shuffle(plain)
    return ''.join(plain)

def execute_command(command,plain,coded):
    print "Running command: bash %s" % command
    proc = subprocess.Popen(("/bin/bash","-c",command),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc.wait()
    stdoutdata = proc.stdout.read()
    stdoutdata += proc.stderr.read()
    output = ""
    for letter in stdoutdata:
        if letter in plain:
            output += coded[plain.find(letter)]
        else:
            output += letter
    
    return output

def handle_client(connection,addr):
    # seed after fork
    random.seed()

    plain = "`1234567890-=~!@#$%^&*()_+[]\{}|;':\",./<>?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    conn.send("You have connected to the Slightly Secure Shell server of Fortress Certifications.\n")
    coded = shuffle_plain(plain)

    command = ""
    conn.send("#>")
    while 1:
        data = conn.recv(1)
        if not data: break
        #is it a del
        if data == "\x7f" or data == "\x08":
            if len(command) > 0:
                command = command[:-1]
            continue
        #is it a return
        if data == "\n" or data =="\r":
            #Run the command
            if len(command) == 0: continue
            conn.send("Running command: '%s'\n" % command)
            cmd_stdout = execute_command(command,plain,coded)
            conn.sendall(cmd_stdout+"\n")
            command = ""
            conn.sendall("Key reset\n")
            coded = shuffle_plain(plain)
            conn.sendall("#>")
        else:
            if data not in plain:
                continue
            command += data
        
        conn.sendall(data)
            
    conn.close()    


#Run the chroot code
#TODO: Define the chroot user and group here
helpers.initialize_chroot(2003,1004)

print "Starting up simple crypto challenge"
listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensock.bind(("0.0.0.0",12433))
print "Listening on port 12433"

#We dont care for zombies
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

listensock.listen(1)
while True:
    (conn,address) = listensock.accept()
    print "Connection accepted from",address
    try:
        pid = os.fork()
    except:
        print "Error occurred when forking. Ignoring"
        continue
        
    if pid == 0:
        #Child Process - handle client then quit
        handle_client(conn,address)
        os._exit(0)
    else:
        #Parent process - Continue accepting connections
        print "Forking off child process PID=%d" % pid
        continue

listensock.close()   
