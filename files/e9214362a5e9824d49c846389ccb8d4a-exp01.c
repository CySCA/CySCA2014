=== snip... ===
void handle_client( int client_socket )
{
    unsigned int FixedVariable = 0xFFFFFFFF;
    unsigned char DestBuffer[16] = {0};
    char secretKey[256];
    unsigned char socketBuffer[SOCKET_BUFFER_SIZE] = {0};
    size_t secretLength = 0;
    int retVal = 0;

    socket_printf( client_socket, "FixedVariable @ %#x. DestBuffer @ %#x\n", &FixedVariable, DestBuffer );

    socket_printf( client_socket, "Please enter text to write to buffer: " );
    retVal = read( client_socket, socketBuffer, SOCKET_BUFFER_SIZE );

    if( retVal <= 0 )
    {
        socket_printf( client_socket, "Error reading input %d.\n", retVal );
        return;
    }

    g_client_socket = client_socket;
    signal( SIGALRM, sigHandler );
    alarm(10);

    strncpy( DestBuffer, socketBuffer, MAX_WRITE_SIZE );
    
    socket_printf( client_socket, "Entered text: %s\n", DestBuffer );
    socket_printf( client_socket, "FixedVariable value: 0x%08X\n", FixedVariable );
    if( FixedVariable == 0x73696854 )
    {
        secretLength = load_flag( secretKey, sizeof(secretKey) );
        socket_printf( client_socket, "Congratulations! Secret key is: %s\n", secretKey );
    }
    else
    {
        socket_printf( client_socket, "Please set FixedVariable to 0x73696854\n" );
    }
    close( client_socket );
}
=== snip... ===
