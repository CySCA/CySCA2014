###############################################################
# This file implements crypto 3 of the CySCA 2014 challenge
###############################################################
from Crypto.Cipher import AES
import os
import sys
import socket
import helpers
import signal
from encodings import hex_codec
iv_size = 4
key = os.urandom(16)

def reset_key(conn):
    key = os.urandom(16)
    conn.send("Key Reset!\n")

def gen_iv():
    iv_nibbles = os.urandom(iv_size).encode("hex")[0:iv_size]
    iv_total = iv_nibbles+"1"*(32-len(iv_nibbles))
    return iv_total.decode("hex")

def encrypt(iv,data):
    pad_bytes = 16-(len(data) % 16)

    if pad_bytes < 16 and pad_bytes > 0: 
        data = data + "X"*pad_bytes

    aes = AES.new(key,AES.MODE_OFB, iv)
    ciphertext = aes.encrypt(data)
    if pad_bytes < 16:
        ciphertext = ciphertext[0:-pad_bytes]

    return ciphertext

def send_banner(conn):
    conn.send("    Welcome to the FortCerts Certified Data Encryption Service\n")
    conn.send("            This program uses very secure encryption\n")
    conn.send("Commands:\nE - Encrypt specified data\nD - Dump service stored data\n")
    conn.send("Output is in format <IV>:<Encrypted Data>\n")

def handle_client(connection,addr):
    reset_key(connection)
    send_banner(connection)

    f = conn.makefile()

    #Get the next command
    cmd = f.readline()
    while len(cmd) <> 0:
        cmd = cmd.strip()
        if len(cmd) == 0:
            conn.send("Invalid command. Bye\n")
            break
        iv = gen_iv() #Generate a new iv

        #Process command
        if cmd[0] == "D":
            ciphertext = encrypt(iv, helpers.load_flag())
            conn.send(iv.encode("hex")[0:iv_size]+":"+ciphertext.encode("hex")+"\n")
            #Reset the key after dumping the encrypted flag
            reset_key(connection)
            cmd = f.readline() #Get next command
            continue
        elif cmd[0] == "E":
            segs = cmd.split(",")
            if len(segs) <> 2 or len(segs[1]) < 1:
                conn.send("Invalid use of encrypt. Usage E,<valuetoencrypt>\n")
            else:
                ciphertext = encrypt(iv, segs[1])
                conn.send(iv.encode("hex")[0:iv_size]+":"+ciphertext.encode("hex")+"\n")
            cmd = f.readline() #Get next command
            continue
        else:
            conn.send("Invalid command. Bye\n")
            break

    #clean up sockets
    f.close()
    conn.close()

#Run the chroot code
#TODO: Define the chroot user and group here
helpers.initialize_chroot(2005,1006)

print "Crypto3: Starting up challenge"
listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensock.bind(("0.0.0.0",1337))
print "Crypto3: Listening on port 1337"

#We dont care for zombies
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

listensock.listen(1)
while True:
    (conn,address) = listensock.accept()
    print "Crypto3: Connection accepted from",address
    try:
        pid = os.fork()
    except:
        print "Crypto3: Error occurred when forking. Ignoring"
        continue

    if pid == 0:
        #Child Process - handle client then quit
        handle_client(conn,address)
        os._exit(0)
    else:
        #Parent process - Continue accepting connections
        print "Crypto3: Forking off child process PID=%d" % pid
        #Close the connected socket in the parent process
        conn.close()
        continue

listensock.close()

