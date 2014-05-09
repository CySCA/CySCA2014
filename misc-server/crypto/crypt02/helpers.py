#!/usr/bin/env python -c
import os
import socket
import sys

#This function initializes the python chroot. if unsuccessful it will exit the python program. if successful it will return as the child process
def initialize_chroot(CHROOT_USER_ID, CHROOT_GROUP_ID):
    print "Current user id is:%d" % os.getuid()
    print "Current group id is:%d" % os.getgid()

    #Setup Chroot
    print "Setting up chroot in /chroots/%d" % CHROOT_USER_ID
    try:
        os.chroot("/chroots/%d" % CHROOT_USER_ID)
        os.chdir("/")
    except:
        print "Changing into chroot failed"
        sys.exit(-1)

    #Set uid and gid
    print "Dropping privs to user %d group %d" %  (CHROOT_USER_ID,CHROOT_GROUP_ID)
    try:
        os.setgid(CHROOT_GROUP_ID)
        os.setuid(CHROOT_USER_ID)
    except:
        print "Dropping user privs failed"
        sys.exit(-1)

    #Fork into a child process
    print "Forking out into a child process"
    try:
        fork_pid = os.fork()
    except:
        print "Fork failed"
        sys.exit(-1)

    if fork_pid != 0:
            #This is the parent proc and no longer needed. Quit
            print "Fork succeeded. Parent process closing"
            sys.exit(-1)

    #This is the child process, return
    return
    
# helper function to return the flag value from chroot    
def load_flag():
	f = open('/flag.txt', 'r')
	data = f.read()
	f.close()
	return data.strip()

