#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <vector>
#include <string>
#include <fstream>  

#include <iostream>
/* Socket header files */
#include <sys/types.h>   
#include <sys/socket.h>

#include <netinet/in.h>

/* Throughout this program, -1 is returned if any error occurs. */
int main (int argc, char **argv){

    if(argc < 2) {
        printf("Format should be: %s <port_number>", argv[0]);
        return -1;
    }
    const char *file_name = argv[1];
    const char *portNumber = argv[2];
    int socketf;
    int connect = 0;
    char ptr[] = "";
    std::vector<char> vec;
    struct sockaddr_in serverAddress, clientAddress;
    socklen_t clientLength;

    /* Creating a socket */
    if((socketf = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Error occurred while creating the socket.");
        return -1;
    }

    memset((char *) &serverAddress, 0, sizeof(serverAddress)); // allocate memory for serverAddress

    /* Address of the socket */
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(atoi(portNumber));  // connect to the port
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    if(bind(socketf,  (struct sockaddr *) &serverAddress, sizeof(serverAddress)) < 0) {
        perror("Error occurred while binding.");
        return -1;
    }
    if(listen(socketf, 5) == -1) {
        perror("Error occurred while listening.");
        return -1;     
    }

    
    clientLength = sizeof(clientAddress);

    int new_socketf;
    new_socketf = accept(socketf, NULL, NULL);  // accept a socket

    if(new_socketf < 0) {
        perror("Error occurred while accepting.");
        return -1;
    }

    /* Program must accept inputs as long as it is terminated by the user. */
    while(1) {
    /* Fetch data */
        if(read(new_socketf, ptr, 1) > 0) {
            /* Construct the string by collecting the bytes one by one. */
            vec.push_back(ptr[0]);
            while(read(new_socketf, ptr, 1) > 0)  vec.push_back(ptr[0]);
            std::string str(vec.begin(), vec.end());
            /* Open the .log file and append the string to it. */
            std::ofstream outfile;
            outfile.open(file_name, std::ios_base::app);
            outfile << str;
            outfile.close(); 
            /* Clear the vector */
            vec.clear();
            /* Accept the socket again to get the next input. */
            new_socketf = accept(socketf, NULL, NULL);
        }
    }


    close(new_socketf);
    close(socketf);
    return 0;
}
