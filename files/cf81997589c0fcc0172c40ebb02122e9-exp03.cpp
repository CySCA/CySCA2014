=== snip... ===
int g_client_socket;

void win(void)
{
    char secret_key[256] = {0x0};

    load_flag(secret_key,sizeof(secret_key));
    socket_printf( g_client_socket, "Success. Your flag is %s\n",secret_key);
}

void handle_client(int client_socket)
{
    char reqData[128] = {0x0};
    CReqObj* reqObj = 0;
    short reqLen = 0;
    bool retValue;
    int recvLen;

    g_client_socket = client_socket;

    signal(SIGALRM, sig_alrm_handler );
    alarm(10);

    recvLen = recv(client_socket,&reqLen,sizeof(reqLen),0);

    if (recvLen == -1 )
        goto cleanup_exit;

    socket_printf(client_socket, "Got request size: %d\n", &recvLen);

    if (reqLen < 0 || reqLen > sizeof(reqData))
    {
        socket_printf(client_socket,"Supplied request length is invalid.\n");
        goto cleanup_exit;
    }

    reqObj = new CReqObj();

    recvLen = recv(client_socket,reqData,reqLen-1,0);
    if (recvLen == -1)
        goto cleanup_exit;

    reqObj->SetRequestData(reqData);
    
    retValue = reqObj->ProcessRequest(); 

    socket_printf(client_socket,"Better luck next time.\n");

cleanup_exit:
    if (reqObj)
        delete reqObj;

    close(client_socket);

    exit(0);
}
=== snip... ===
