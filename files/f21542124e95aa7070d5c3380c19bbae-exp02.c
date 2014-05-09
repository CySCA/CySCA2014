=== snip... ===
#define RESP_PREFIX "Nice to meet you "
#define RANDOM_RANGE 0xFFFFF
void handle_client(int client_socket)
{
    char* memBuf;
    int* pWinning;
    unsigned char socketBuffer[SOCKET_BUFFER_SIZE] = {0};
    char secretKey[256];
    size_t secretLength = 0;
    unsigned char destBuffer[MAX_LEN] = {0};
    int retVal = 0;

    g_client_socket = client_socket;

    memBuf = malloc(RANDOM_RANGE);
    if (memBuf == NULL)
    {
        socket_printf( client_socket, "ERROR: Unable to allocate memory.\n");
        return;
    }

    pWinning = memBuf + (GetRandomNumber() % (RANDOM_RANGE-4));
    *pWinning = 0x12345678;
    memBuf = NULL;

    while (1)
    {
        socket_printf( client_socket, "Hello, what is your name?\n" );
        retVal = read( client_socket, socketBuffer, SOCKET_BUFFER_SIZE );
        if( retVal <= 0 )
        {
            socket_printf( client_socket, "Error reading input %d.\n", retVal );
            return;
        }

        signal( SIGALRM, sigHandler );
        alarm(30);

        strcpy( destBuffer, RESP_PREFIX);
        snprintf( destBuffer+sizeof(RESP_PREFIX)-1, MAX_LEN-sizeof(RESP_PREFIX), socketBuffer );
        socket_printf( client_socket, "%s\n", destBuffer );

        if( *pWinning == 0x31337BEF )
        {
            secretLength = load_flag( secretKey, sizeof(secretKey) );
            socket_printf( client_socket, "Today is your lucky day! Your key is: %s\n", secretKey );
            return;
        }
        else
        {
            socket_printf( client_socket, "Sorry, today is not your lucky day.\n");
        }

    }
    close( client_socket );
}

=== snip... ===
