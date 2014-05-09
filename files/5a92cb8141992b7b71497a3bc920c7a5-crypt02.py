=== snip... ===
def compress(d):
	c = zlib.compressobj()
	return(c.compress(d) + c.flush(zlib.Z_SYNC_FLUSH)).encode("hex")

def encrypt(aes,d):
	return aes.encrypt(d).encode("hex")

def handle_client(conn, addr):
	AESKey = os.urandom(32)
	ctr = Counter.new(128)

	aes = AES.new(AESKey, AES.MODE_CTR, counter=ctr)

	BANNER = "\t\tWelcome to the Keygen server.\n\t\t"
	BANNER += "="*30
	BANNER += "\n[+]All access is monitored and any unauthorised access will be treated as CRIME\n"
	conn.send(BANNER)

	SECRET = 'Key:' + helpers.load_flag()

	data = conn.recv(2048).strip()

	while len(data):
		data = compress(SECRET + data)
		data = encrypt(aes, data)

		conn.send(data)

		data = conn.recv(2048).strip()

	conn.close()
=== snip... ===
