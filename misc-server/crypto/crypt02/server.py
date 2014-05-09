#!/usr/bin/python

import helpers
import socket
import zlib			#for the compression
from Crypto.Cipher import AES	#for the encryption
from Crypto.Util import Counter	#for the encryption
import os
from encodings import hex_codec
import signal

#this is where the compression happens, d is the data sent from the user combined with the secret value
def compress(d):
	c = zlib.compressobj()

	#compressing the secret key with the data supplied from the user
	return(c.compress(d) + c.flush(zlib.Z_SYNC_FLUSH)).encode("hex")

def encrypt(aes,d):
	return aes.encrypt(d).encode("hex")

def handle_client(conn, addr):

	#the actual AES key used 16 bytes
	AESKey = os.urandom(32)
	
	ctr = Counter.new(128)

	#create a new AES object that uses the above details CTR mode makes it a stream
	#cipher I believe
	aes = AES.new(AESKey, AES.MODE_CTR, counter=ctr)

	#the banner that the players are greeted with
	BANNER = "\t\tWelcome to the Keygen server.\n\t\t"
	BANNER += "="*30
	BANNER += "\n[+]All access is monitored and any unauthorised access will be treated as CRIME\n"

	SECRET = 'Key:' + helpers.load_flag()

	#print the banner
	conn.send(BANNER)

	#get input from the client 2048 is arbitrary
	data = conn.recv(2048).strip()

	#while the client continues to send us stuff
	while len(data):
		data = compress(SECRET + data)

		#encrypt the data using AES stream mode
		data = encrypt(aes, data)

		#send the hex representation to the client
		conn.send(data)

		#try to get some more data from the client, if they want to continue,			
		data = conn.recv(2048).strip()

	#client has gone
	conn.close()

#Run the chroot code
#TODO: Define the chroot user and group here
helpers.initialize_chroot(2004,1005)

print "Starting up simple crypto challenge"
listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensock.bind(("0.0.0.0",9999))
print "Listening on port 9999"

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
        #Close the connected socket in the parent process
        conn.close()
        continue

listensock.close()   
