=== snip... ===
void handle_client(int client_socket)
{
    unsigned char hash[SHA_DIGEST_LENGTH];
    unsigned char secret_hash[SHA_DIGEST_LENGTH];

    char secret_key[256];
    char data[256] = {0};

    sendline(client_socket, "Welcome to the SHA password oracle.\n");
    sendline(client_socket, "Enter your password:");

    if (recvline(client_socket, data, sizeof(data)) == -1)
        return;

    // SHA the entered password
    SHA1(data, strlen(data), hash);

    // Load and SHA the secret key
    size_t secret_length = load_flag(secret_key, sizeof(secret_key));
    SHA1(secret_key, secret_length, secret_hash);

    // Compare the two hashes and determine if the password is correct
    if (strncmp(secret_hash, hash, SHA_DIGEST_LENGTH) == 0) {
        char buf[512] = {0};
        snprintf(buf, sizeof(buf)-1, "Congratulations: The key is %s", secret_key);
        sendline(client_socket, buf);
    } else {
        char secret_hash_str[80] = {0};
        char hash_str[80] = {0};
        char buf[512] = {0};

        bytes_to_string((unsigned char*)secret_hash, secret_hash_str, sizeof(secret_hash_str));
        bytes_to_string((unsigned char*)hash, hash_str, sizeof(hash_str));

        snprintf(buf, sizeof(buf)-1, "Your hash %s does not match the secret hash %s", hash_str, secret_hash_str);
        sendline(client_socket, buf);
    }   

    close(client_socket);
}
=== snip... ===
