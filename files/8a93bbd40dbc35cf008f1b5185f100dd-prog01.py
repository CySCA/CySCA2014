=== snip... ===
def jumble(word):
	return ''.join(random.sample(word,len(word)))  	

def handle_client(conn,addr):
	WORDSAMPLESIZE 	= 25
	CORRECTANSWERS 	= 50
	ELAPSEDTIME 	= 60

	BANNER = "\t\tWelcome to the jumbled word server.\n\t\t"
	BANNER += "="*30
	BANNER += "\n[+] Unjumble %d words sequentially within %d seconds.\n" % (CORRECTANSWERS, ELAPSEDTIME)	
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
		randomList = random.sample(dictList, WORDSAMPLESIZE)
		conn.send("Wordlist: %s\n" % repr(randomList))
		time.sleep(0.2)

		serverWord = randomList[random.randint(0,len(randomList)-1)]
		conn.send("Jumbled word: %s\n" % jumble(serverWord))		
		time.sleep(0.2)

		conn.send("Enter unjumbled word: \n")
		clientWord = conn.recv(1024)
		
		if serverWord.strip() == clientWord.strip():
			correctCounter += 1 
	
	elapsed = (int(time.time()) - start)
	if correctCounter == CORRECTANSWERS and elapsed < ELAPSEDTIME:
		conn.send(helpers.load_flag())
	elif correctCounter == CORRECTANSWERS:
		conn.send("You unjumbled all the words but took to long")
	else:
		conn.send("You got %d / %d words correct" % (correctCounter,CORRECTANSWERS))
				
	conn.close()
=== snip... ===
