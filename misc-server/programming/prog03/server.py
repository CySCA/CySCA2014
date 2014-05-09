import numpy
from numpy.random import random_integers as rand
from itertools import product
import numpy.random
import socket
import signal
import sys
import os
from pygraph.algorithms.minmax import shortest_path
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
import helpers

M_PATH = 0
M_WALL = 1
M_UP = 2
M_DOWN = 3
M_KEY = 4
M_DOOR = 5

def get_id(x,y,z):
    return "%d:%d:%d" % (x,y,z)
    
def add_graph(gr, Z, level):
    width = Z.shape[0]
    height = Z.shape[1]
    for x, y in product(range(width), range(height)):
        # create new nodes
        node = get_id(x,y,level)        
        if not gr.has_node(node):
            gr.add_node(node)
            
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (abs(i+j) == 1): continue
            if not (0 <= x + i < width): continue
            if not (0 <= y + j < height): continue
            # don't connect edges to walls
            if Z[y+j,x+i] == M_WALL: continue
            if Z[y,x] == M_WALL: continue
            
            # create an edge
            node2 = get_id(x+i,y+j,level)        
            if not gr.has_node(node2):
                gr.add_node(node2)
            if not gr.has_edge((node, node2)):
                gr.add_edge((node, node2))
        
def maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=int)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make isles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z

def setnode(Z, node_type):
    (x,y) = emptynode(Z)
    Z[y,x] = node_type
    return (x,y)

def emptynode(Z):
    while True:
        x = rand(1,Z.shape[0]-1)
        y = rand(1,Z.shape[1]-1)
        if Z[y,x] == 0:
            return (x,y)

def findnode(Z, node_type):
    for y in range(Z.shape[0]):
        for x in range(Z.shape[1]):
            if Z[y,x] == node_type:
                return (x,y)

    
def handle_client(conn,addr):
    numpy.random.seed()
    NUM_LEVELS = 10
    COMMAND_LIST = ['north', 'south', 'east', 'west', 'up', 'down', 'pickup', 'escape']

    conn.send('Please wait while the map loads...\n')

    levels = {}
    gr = graph()
    key_level = rand(NUM_LEVELS-3,NUM_LEVELS-1)
    door_level = 0
    for i in range(NUM_LEVELS):
        levels[i] = maze(25, 25, 1, 1)
        add_graph(gr, levels[i], i)
        if i > 0:
            (x_d,y_d) = setnode(levels[i], M_DOWN)
            down = get_id(x_d, y_d, i)
            gr.add_edge((up, down))
        if i < NUM_LEVELS-1:
            (x_u,y_u) = setnode(levels[i], M_UP)
            up = get_id(x_u, y_u, i)
        if i == key_level:
            (x, y) = setnode(levels[i], M_KEY)
            key = get_id(x, y, i)
        if i == door_level:
            (x, y) = setnode(levels[i], M_DOOR)
            door = get_id(x, y, i)
            
    st,weights = shortest_path(gr, key)
    distance = weights[door]
    collapse = distance + 5

    start_z = NUM_LEVELS/2
    (start_x, start_y) = emptynode(levels[start_z])
    
    c_x = start_x
    c_y = start_y
    c_z = start_z
    
    player_key = False

    conn.send('Map loaded.\n')
    
    while True:
        node = levels[c_z][c_y,c_x]
        if node == M_UP:
            conn.send('There are stairs heading upward.\n')
        if node == M_DOWN:
            conn.send('There are stairs heading downward.\n')
        if node == M_KEY:
            conn.send('There is a key here.\n')
        if node == M_DOOR:
            conn.send('There is a locked door here.\n')        
        
        data = conn.recv(1024).strip()
        commands = data.split('\n')

        for command in commands:
            if not command in COMMAND_LIST:
                conn.send('Invalid command: %s. Possible commands include are: %s\n' % (command, COMMAND_LIST))
                continue
            if command == 'pickup':
                if player_key:
                    conn.send('You already have the key.\n')
                else:
                    if checknode(levels[c_z], c_x, c_y, M_KEY):
                        conn.send('You picked up the key.\n')
                        conn.send('The ceiling starts to collapse.\n')
                        player_key = True
                    else:
                        conn.send('No key here.\n')
            elif command == 'escape':
                if checknode(levels[c_z], c_x, c_y, M_DOOR):
                    if player_key:
                        conn.send('YOU ESCAPED!\n')
			conn.send('Key: %s' % helpers.load_flag())
                    else:
                        conn.send('You need the key to unlock the door.\n')
                else:
                    conn.send('No door here.\n')
            elif command == 'north':
                if checknode(levels[c_z], c_x, c_y-1, M_WALL):
                    conn.send('There is a wall there.\n')
                else:
                    conn.send('You moved north.\n')
                    c_y = c_y-1
            elif command == 'south':
                if checknode(levels[c_z], c_x, c_y+1, M_WALL):
                    conn.send('There is a wall there.\n')
                else:
                    conn.send('You moved south.\n')
                    c_y = c_y+1
            elif command == 'west':
                if checknode(levels[c_z], c_x-1, c_y, M_WALL):
                    conn.send('There is a wall there.\n')
                else:
                    conn.send('You moved west.\n')
                    c_x = c_x-1
            elif command == 'east':
                if checknode(levels[c_z], c_x+1, c_y, M_WALL):
                    conn.send('There is a wall there.\n')
                else:
                    conn.send('You moved east.\n')
                    c_x = c_x+1
            elif command == 'up':
                if checknode(levels[c_z], c_x, c_y, M_UP):
                    conn.send('You moved upstairs.\n')
                    c_z = c_z + 1
                    c_x, c_y = findnode(levels[c_z], M_DOWN)
                else:
                    conn.send('No stairs upward here.\n')
            elif command == 'down':
                if checknode(levels[c_z], c_x, c_y, M_DOWN):
                    conn.send('You moved downstairs.\n')
                    c_z = c_z - 1
                    c_x, c_y = findnode(levels[c_z], M_UP)
                else:
                    conn.send('No stairs downward here.\n')
                        
            if player_key:
                collapse -= 1
                conn.send('Get out of here!\n')

            if collapse == 10:
                conn.send('The ceiling is about to collapse!\n')
            
            if collapse == 50:
                conn.send('Large pieces of debris fall from the ceiling.\n')
                
            if collapse == 100:
                conn.send('Hurry!\n')
            
            if collapse == 0:
                conn.send('The ceiling collapses and crushes you. You are dead.\n')
                conn.send('You are dead.\n')
                return        

def checknode(Z, x, y, node_type):
    return Z[y,x] == node_type

#Run the chroot code
#TODO: Define the chroot user and group here
helpers.initialize_chroot(2009,1010)

print "Starting up maze server"
listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensock.bind(("0.0.0.0",7788))
print "Listening on port 7788"

#We dont care for zombies
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

listensock.listen(1)
while True:
    (conn,address) = listensock.accept()
    print "Connection accepted from",address
    try:
        pid = os.fork()
    except NameError as e:
        print "NameError %s" % format(e.message)
    except:
        print "Error occurred when forking: %s. Ignoring" % sys.exc_info()[0]
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
