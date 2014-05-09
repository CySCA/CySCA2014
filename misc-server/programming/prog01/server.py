#!/usr/bin/env python

import socket
import helpers
import time
from random import randrange
import random
import re
import os
import signal

def jumble(word):
	return ''.join(random.sample(word,len(word)))  	

def handle_client(conn,addr):
	WORDSAMPLESIZE 	= 25
	CORRECTANSWERS 	= 50
	ELAPSEDTIME 	= 60

	# seed after fork
	random.seed()

	#the banner that the players are greeted with
	BANNER = "\t\tWelcome to the jumbled word server.\n\t\t"
	BANNER += "="*30
	BANNER += "\n[+] Unjumble %d words sequentially within %d seconds.\n" % (CORRECTANSWERS, ELAPSEDTIME)	

	#print the banner
	conn.send(BANNER)

	dictList = []
	ins = open( "words.txt", "r" )
	for line in ins:
		dictList.append(line.strip())
	ins.close()

	time.sleep(0.2)
	correctCounter=0
	start = int(time.time())

	for x in range(0,CORRECTANSWERS):
		
		#Send random word list range
		randomList = random.sample(dictList, WORDSAMPLESIZE)
		conn.send("Wordlist: %s\n" % repr(randomList))
		
		time.sleep(0.2)
		#Send random jumbled word
		serverWord = randomList[random.randint(0,len(randomList)-1)]
		conn.send("Jumbled word: %s\n" % jumble(serverWord))
		
		time.sleep(0.2)
		#Receive jumbled word
		conn.send("Enter unjumbled word: \n")
		clientWord = conn.recv(1024)
		
		if serverWord.strip() == clientWord.strip():
			correctCounter+=1
	
	elapsed = (int(time.time()) - start)
	print elapsed
	if correctCounter == CORRECTANSWERS and elapsed < ELAPSEDTIME:
		conn.send(helpers.load_flag())
	elif correctCounter == CORRECTANSWERS:
		conn.send("You unjumbled all the words but took to long")
	else:
		conn.send("You got %d / %d words correct" % (correctCounter,CORRECTANSWERS))
				
	conn.close()

#Run the chroot code
#TODO: Define the chroot user and group here
helpers.initialize_chroot(2008,1009)

print "Starting up simple crypto challenge"
listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensock.bind(("0.0.0.0",5050))
print "Listening on port 5050"

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

