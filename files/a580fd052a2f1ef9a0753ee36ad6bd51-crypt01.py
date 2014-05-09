=== snip... ===
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
    
def handle_client(conn,addr):
    plain = "`1234567890-=~!@#$%^&*()_+[]\{}|;':\",./<>?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    conn.send("You have connected to the Slightly Secure Shell server of Fortress Certifications.\n")
    coded = shuffle_plain(plain)

    command = ""
    conn.send("#>")
    while 1:
        data = conn.recv(1)
        if not data: break

        if data == "\x7f" or data == "\x08":
            if len(command) > 0:
                command = command[:-1]
            continue
        if data == "\n" or data =="\r":
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
=== snip... ===
