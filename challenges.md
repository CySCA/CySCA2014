
## Web Application Pentest

### Club Status

80 points

Only VIP and registered users are allowed to view the Blog. Become VIP to gain access to the Blog to reveal the hidden flag.



### Om nom nom nom

160 points

Gain access to the Blog as a registered user to reveal the hidden flag.



### Nonce-sense

220 points

Retrieve the hidden flag from the database.



### Hypertextension

260 points

Retrieve the hidden flag by gaining access to the caching control panel.



### Injeption

280 points

Reveal the final flag, which is hidden in the /flag.txt file on the web server.



## Corporate Network Pentest

### Friend Zone

80 points

Reveal a list of hosts in the fortcerts domain and find the hidden flag.



### Gone Phishin

160 points

Gain access to the corporate network and retrieve the flag from the users Desktop.



### "Gone in 20 Seconds"

220 points

On the current host, gain privileged access and retrieve the flag from C:\\Windows\\System32\\config



### Total Recall

260 points

Gain access to the IT teams credentials file and retrieve the flag.



### Private Parts

280 points

Gain privileged access on the domain controller and retrieve the flag.



## Android Forensics

You will require the following files:
* <a href="/files/99de51b8da4623ddc2fcc18b9063f81e.7z">99de51b8da4623ddc2fcc18b9063f81e.7z</a> - The Android 4.1.2 (Goldfish 2.6.29 Kernel) memory dump
* <a href="/files/goldfish-2.6.29.zip">goldfish-2.6.29.zip</a> - Volatility profile that will enable the memory dump to be analysed.
* <a href="/files/system_framework.7z">system_framework.7z</a> - Files from framework the folder under the /system partition. These are required to decompile optimised Dalvik executables for this version (API 16) of Android.

Instructions to start the analysis:

1. Install the latest volatility from subversion.
2. svn checkout http://volatility.googlecode.com/svn/trunk/ volatility-read-only
3. Copy the goldfish-2.6.29.zip into volatility-read-only/volatility/plugins/overlays/linux/
4. Extract the memory dump

### Flappy Bird

120 points

Identify the suspicious app on the device

a) Identify the PID of the suspicious app on the phone.

b) What UID is associated with this process?

c) When did the process start?

Note the processes with PIDs 1454, 1461, 1468 are for dumping memory and can be ignored.

Example answer format: [1234] [4321] [0000-00-00 00:00:00 UTC+0000]



### Tower of Medivh

120 points

Provide the CVE for the vulnerability that was used to allow the installation of this package.

Example answer format: [CVE-2000-0001]



### Wrath

180 points

Identify additional payload stages 

a) What are the file paths for the second and third Java stages of the malware? 

b) What are the file sizes of these two files (in bytes)?

c) What is the publicly named malware used in both stages?

Example answer format: [/dir/dir/filename1.ext | /dir/dir/filename2.ext] [12345 | 54321] [MalwareRAT]



### Scams Through The Portal

180 points

Investigate the attack vector

a) Provide the full path to the malicious app's original location on the phone.

b) Provide the IP for where the malware was initially downloaded.

c) What is the email address of the person who is responsible for this compromise?

Example answer format: [/dir/dir/filename.ext] [127.0.0.1] [email@domain.com]



### hunter2

200 points

Information on files exfiltrated

a) Where were the files copied to before they were stolen?

b) What were the credentials that were stolen?

c) What was the full path to the PDF document that was exfiltrated?

Example answer format: [/dir/dir/stagedir/] [username/password] [/dir/dir/filename.ext]



### Electronic Sheep

230 points

Analysis on the malicious application

a) What is the malicious domain and port associated with the malware?

b) What is the <strong>existing</strong> Class method (Java) that was modified to jump to the malicious code?

Example answer format: [domain.com:1234] [methodName()]



## Random

### Pulp Fiction

120 points

RL Forensics Inc. has contracted Fortcerts to recover information stored in this bitmap. Both companies failed to recover the information but they identified that it was encrypted with AES-ECB. Can you recover the information in the encrypted bitmap?

<a href="/files/438b8e5411a303d950d0cbe1bfe2230b-rand01">438b8e5411a303d950d0cbe1bfe2230b-rand01</a>



### Spanish Trout

200 points

Fortcerts has been hired by Mad Programming Skillz Pty. Ltd. to perform source code review to find vulnerabilities in the password checking algorithm that they use in many of their products. Fortcerts does not have the expertise to do c code auditing so they have asked you to take a look. Try find any vulnerabilities and capture the flag to demonstrate that an attacker could exploit the identified vulnerabilities. The test code is running at 172.16.1.20:12345

Source: <a href="/files/008c71693fbf6c53ccebc5560cff177c-rand02.c">008c71693fbf6c53ccebc5560cff177c-rand02.c</a>



### Reed Between The Lines

280 points

In an RL Forensics Inc. case contracted out to Fortcerts, an image has been found on a suspects computer. Analysts believe there is corrupted information secretly hidden in the image. As a "computer expert" they want you to recover the data from this image

<a href="/files/dd02a42c12ce34edac8022f292dc8c96-rand03.jpg">dd02a42c12ce34edac8022f292dc8c96-rand03.jpg</a>



## Reverse Engineering

### U JAD BRO?

120 points

Staff from Terribad Corp have forgotten the password for their propriety data protection Java application. They need you to retrieve the data stored in the application and submit it. 

<a href="/files/0a736429aacc4b42e76120c53ea0ec7d-re01.jar">0a736429aacc4b42e76120c53ea0ec7d-re01.jar</a>



### Knock Knock

200 points

Terribad Corp has provided a binary which they think is the "next big thing" in security. They would like to get it certified as a secure product. We need you to reverse engineer the algorithm to understand what it does. Once you have done this, a test server is running at 172.16.1.20:3422 to allow you to prove you completely recovered the algorithm. 

Binary: <a href="/files/488f866ad090d0843657f322e516168a-re02">488f866ad090d0843657f322e516168a-re02</a>



### Forever Alone

280 points

Terribad Corp has lost the client component of a legacy application that they no longer have the source code for. They want you to reverse engineer the 
provided server binary and build a client to interact with the server. Once you have done this, the server binary is running on 172.16.1.20 to 
test your client implementation against. 

Binary: <a href="/files/10cb2de913234d75c8aa0d1d6219afec-re03">10cb2de913234d75c8aa0d1d6219afec-re03</a>



## Crypto

### Standard Galactic Alphabet

120 points

Perform a white box evaluation of the custom encryption used in Fortcerts "Slightly Secure Shell" program. Identify any vulnerabilites in their implementation and demonstrate that they can be exploited to gain confidential information. The server is running at 172.16.1.20:12433 

Source: <a href="/files/a580fd052a2f1ef9a0753ee36ad6bd51-crypt01.py">a580fd052a2f1ef9a0753ee36ad6bd51-crypt01.py</a>



### Compression Session

200 points

Perform a white box evaluation of the Fortcerts highly secure key generation server. Identify and exploit any vulnerabilities in the implementation that will lead to a disclosure of secret data. The server is running at 172.16.1.20:9999

Source: <a href="/files/5a92cb8141992b7b71497a3bc920c7a5-crypt02.py">5a92cb8141992b7b71497a3bc920c7a5-crypt02.py</a>



### Chop Suey

280 points

Senior staff at Fortcerts have expressed objections to the use of white box evaluation methodology with the argument "real attackers won't have source code access". Perform a black box evaluation of the Fortcerts very secure encryption service. Diagnose and identify any crypto vulnerabilities in the service that can be used to recover encrypted data. The very secure encryption service is running at 172.16.1.20:1337




## Exploitation

### The Fonz

120 points

Perform a review of the supplied source code for Quick Code Ltd. to identify any vulnerabilities. A server has been set up for you to exploit the identified vulnerabilities for the customer at 172.16.1.20:20000

Source: <a href="/files/e9214362a5e9824d49c846389ccb8d4a-exp01.c">e9214362a5e9824d49c846389ccb8d4a-exp01.c</a>
Binary: <a href="/files/9c37e1b5e0607c041e40aa6ac43352a7-exp01">9c37e1b5e0607c041e40aa6ac43352a7-exp01</a>



### "Matt Matt Matt Matt"

200 points

Perform a review of the supplied source code for Quick Code Ltd. to identify any vulnerabilities. A server has been set up for you to exploit the identified vulnerabilities for the customer 172.16.1.20:20001

Source: <a href="/files/f21542124e95aa7070d5c3380c19bbae-exp02.c">f21542124e95aa7070d5c3380c19bbae-exp02.c</a>
Binary: <a href="/files/c0599033e8f6f06f5ed8d8acc5ac50cf-exp02">c0599033e8f6f06f5ed8d8acc5ac50cf-exp02</a>



### A Bit One Sided

280 points

Perform a review of the supplied source code for Quick Code Ltd. to identify any vulnerabilities. A server has been set up for you to exploit the identified vulnerabilities for the customer at 172.16.1.20:21320

Source: <a href="/files/cf81997589c0fcc0172c40ebb02122e9-exp03.cpp">cf81997589c0fcc0172c40ebb02122e9-exp03.cpp</a>
Binary: <a href="/files/efed50a053ba74f8b58794d2690ecaf3-exp03">efed50a053ba74f8b58794d2690ecaf3-exp03</a>



## Shellcode

### Missing Missy

120 points

The first task Mad Programming Skillz Pty. Ltd have for you requires that you write a function in shellcode that sets the EAX register to the memory address of the first instruction of your shellcode. The code to be tested is running on the server at 172.16.1.20:9090. The server will provide more information on your task. Your test MUST return execution to the program.



### X97:L97

200 points

Mad Programming Skillz Pty. Ltd have created code to dynamically allocate a function that returns a flag, obfuscate it and place it randomly in memory to improve software security. To ensure this works correctly, they need you to write a test with shellcode that will locate the function within the specified memory range, deobfuscate and return control to it. The code is running at 172.16.1.20:16831. The server will provide more information on your task. 



### Stop, Rop and Roll

280 points

The last task that Mad Programming skills have provided requires that you test a range of functionality in a binary provided by them. The development of this binary had no thought for future testing so DEP was enabled, this means you will need to add a pivot and ROP in addition the test shellcode to return the flag. The code is running at 172.16.1.20:22523. The server will provide more information on your task.  

Binary: <a href="/files/8305f5c99ba1d89802940f6e68f802f5-sc03">8305f5c99ba1d89802940f6e68f802f5-sc03</a>




## Network Forensics

### Not Enough Magic

120 points

You have been supplied with the following network capture with a note mentioning that the suspect has previously hidden information, although basically. Analyse the network capture to recover the flag hidden by the suspect.

<a href="/files/86590ed37efccf55b78f404ae6be09f0-net01.pcap">86590ed37efccf55b78f404ae6be09f0-net01.pcap</a>



### Notwork Forensics

200 points

You have been given a network capture file of an exchange between two suspected criminals. Analyse the session and files transferred to recover the suspects flag. 

<a href="/files/c18493dcc4281aef5d3c4b24d674d8e3-net02.pcap">c18493dcc4281aef5d3c4b24d674d8e3-net02.pcap</a>



### AYBABTU

280 points

RL Forensics Inc. has supplied a network capture from one of their customers that was infected with trojan malware. The customer was able to capture a command and control session of the trojan communicating with the criminals server. They would like to know what data was stolen by criminals. Analyse the communications, determine the custom protocol and extract the stolen information to reveal the flag 

<a href="/files/74db9d6b62579fea4525d40e6848433f-net03.pcap">74db9d6b62579fea4525d40e6848433f-net03.pcap</a>



## Mad Coding Skillz

### Jeremy's Iron

120 points

FortCerts needs you to write a program to test the functionality of a customers anagram program. Write a program that will unscramble the given word from a list of words and return it to the server. To be sure that the testing is reliable you will need to do this multiple times before the flag is revealed. The customer program is running at 172.16.1.20:5050 

Source: <a href="/files/8a93bbd40dbc35cf008f1b5185f100dd-prog01.py">8a93bbd40dbc35cf008f1b5185f100dd-prog01.py</a>



### Autobalanced

200 points

FortCerts is certifying a server program that generates challenges for authentication purposes. Write a program that will solve the challenges provided by the server. To ensure results are consistent and repeatable you will need to solve a number of challenges before you are authenticated and gain the flag. The server program is running at 172.16.1.20:9876



### Spelunking!

280 points

FortCerts are working on a breakthrough project known as project EVATAR. Using the EVATAR interface, players use neural brain circuit interferometry to control a real person trying to escape from a dangerous scenario. In this case, the scenario is a person stuck in a cave (with steps, apparently). Write a program to control your EVATAR to find the key and escape the maze. Watch your EVATAR's step though, the ceiling may be unstable. The project EVATAR access interface is located at 172.16.1.20:7788. Also don't tell anyone, it's super hush hush.


