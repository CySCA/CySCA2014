#!/usr/bin/python
################################################################################################
# This python file implements the server for programming challenge 2 of the CySCA 2014 challenge
################################################################################################

import socket
import random
import signal
import helpers
import os

LENGTH  = 28
RANGE   = 1170 
SIZE    = (LENGTH * RANGE * 2 + 1)
Q = [ ([0] * (LENGTH + 1)) for _ in range( SIZE + 1 ) ] 
lines = []
possible = []

def get_flag():
    try:
        f = open( "flag.txt","r")
        flagcontent = f.readline()
        f.close()
    except:
        flagcontent = "ERROR: Unable to load flag. Talk to ExCON"

    return flagcontent

#This function pre-populates the lines with content from output.txt
def open_lines():
    f = open( "pregen.txt", "r" )

    for l in f.readlines():
        n = l.rstrip().split( " " )
        lines.append( " ".join( n[1:] ) )
    f.close()

def answer_length( length, values, s, n, b, a ):
        # fail case
        if length <= 0:  
                return False

        # base case
        if values[n] + s == 0 and length == 1:
                return True

        # exclude
        if Q[s-b][n+1] and answer_length( length, values, s, n+1, b, a ):  
                return True;
     
        # include
        temp = s + values[n]
        if temp >= b and temp <= a and Q[s-b+values[n]][n+1] and answer_length( length-1, values, s+values[n], n+1, b, a ): 
                return True

def subsetsum_matrix( values, a, b ):
        # zero matrix
        for s in range( SIZE ):
                for n in range( LENGTH + 1 ):
                        Q[s][n] = 0 

        # populate sum values bottom up
        for n in range( len(values) - 1, -1, -1 ):
                for s in range( b, a + 1 ):
                        self = values[n] + s == 0
                        exclude = Q[s-b][n+1]
                        include = False
                        temp = s + values[n]
                        if temp >= b and temp <= a:  
                                include = Q[s-b+values[n]][n+1]
                        Q[s-b][n] = self or exclude or include
        return Q[-b][0]


def listen_for_clients():
    #init chroot
    helpers.initialize_chroot(2014,1015)

    # setup server
    listensock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listensock.bind( ( "0.0.0.0", 9876 ) )
    listensock.listen( 5 )

    #Quietly ignore zombie children
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print( "PROG02: socket, bind and listen complete" )

    while True:
        print( "PROG02: Waiting for client" )       
        ( client, address ) = listensock.accept()
        print( "PROG02: Got new client {0}".format( address ) )

        #Fork the processes
        try:
            pid = os.fork()
        except:
            print "PROG02: Error occurred during forking. Ignoring"
            continue

        if pid == 0:
            #Child fork - Close the server socket handle, Reseed random and process the client
            listensock.close()
            random.seed()
            ch = ClientHandler( client )
            ch.run()
            print( "PROG02: Handling client" )
        else:
            #Parent fork - Close the client socket and continue
            print "PROG02: Forked off child process with id %d" % pid
            client.close()
            continue

class ClientHandler():
    def __init__( self, socket ):
        self.s = socket
    
    def timeout_handler(self, signum, frame):
        self.send( "Timeout. Challenge-Response handshake must complete in 8 seconds\n" )
        exit()

    def run( self ):
        # send banner
        self.s.send( "Welcome to the Fortcerts secure server. This server is protected by a challenge response authentication method. At Fortcerts we do not believe in security by obscurity: the response must sum to zero. Possible responses are a list of integers separated by spaces or the string 'no solution' (because the server is ultra-secure sometimes there may not be a solution). Generating challenge...\n\n" )
        

        #Pregenerate solutions
        self.sample = [ lines[i] for i in random.sample( xrange( len(lines)), 10 ) ]
        self.lengths = []
        self.solutions = []
        for s in self.sample:
            nums = [ int(n) for n in s.split(" ") ]
            a = 0
            b = 0
            for n in nums:
                if n > 0:
                    a += n
                else:
                    b += n
            success = subsetsum_matrix( nums, a, b )
            for i in range( 2 ):
                length = random.randrange( 10, 19 )
                success = success and answer_length( length, nums, 0, 0, b, a )
                if success:
                    break
            self.solutions.append( success ) 
            self.lengths.append( length )
        
        #Setup timeout
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(8)

        # Process user output
        self.handle_client()

        self.s.close()
    
    def send( self, msg ):
        #print( msg )
        self.s.send( msg )

    def handle_client( self ):
        for i in range( 10 ):
            original = [int(x) for x in self.sample[i].split(" ")]
            length = self.lengths[i]
            success = self.solutions[i]
    
            # send line
            self.send( "Round: {0}\nRequired response length: {1}\nChallenge: {2}\n".format( i + 1, length, self.sample[i] ) )
    
            # await response
            r = self.s.recv( 1000 ).rstrip()
            #print( "got: " + r )
            
            # check none
            if r == "no solution":
                if not success:
                    self.send( "Correct.\n" )
                    continue
                else:
                    self.send( "Incorrect - There is a solution.\n" )
                    self.s.close()
                    exit()
    
            # parse response
            try:
                answer = [int(x) for x in r.split( " " )]
            except:
                self.send( "Could not parse answer. Format should be integers separated by spaces or 'no solution'.\n" );
                self.s.close()
                exit()
    
            # check each val is in original
            for v in answer:
                if v not in original:
                    self.send( "{0} not in original set or has been used more than once.\n".format( v ) )
                    self.s.close()
                    exit()
                else:
                    # remove to not allow duplicates
                    original.remove( v )
            
            # check length of response
            if len( answer ) != length:
                self.send( "Required response length {0}, you had length {1}\n".format( length, len( answer ) ) )
                self.s.close()
                exit()

            # check sums to zero
            if sum( answer ) != 0:
                self.send( "Sum should be zero - sum is: {0}.\n".format( sum( answer ) ) )
                self.s.close()
                exit()
            
            self.send( "Correct.\n" )
    
        #We get here if we have solved 10 challenges
        self.send( "Flag: "+get_flag()+"\n" );
        self.s.close()
        exit()

if __name__ == "__main__":
    open_lines()
    listen_for_clients()
