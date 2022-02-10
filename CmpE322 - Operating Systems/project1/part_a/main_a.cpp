#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>  // for pid_t
#include <sys/wait.h>
#include <string>   // c++ string
#include <iostream>
#include <fstream>  // writing to a file
#include <vector>
#include <string>

/* Define read and write points of the pipe as 0 and 1 for simplicity */
/* Throughout this source code, for the erroneous cases, -1 is returned. */
#define READ_FD     0
#define WRITE_FD    1

int main(int argc, char const *argv[]) {
    /* Executable path and output file path are taken from the command line arguments. */
    const char* executable = argv[1];
    const char* output = argv[2];

    pid_t childpid;
    /* 3 pipes will be created. 
    First pipe : parent-to-child for writing the input 
    Second pipe : child-to-parent STDOUT for taking the result of the calculation (if successful) 
    Third pipe: child-to-parent STDERR for taking the text error printed out by the child */
    int p2c[2];
    int c2pSTDOUT[2];
    int c2pSTDERR[2];

    /* Return -1 if you encounter any error while creating the pipe and forking.*/
    if(pipe(p2c) < 0 || pipe(c2pSTDOUT) < 0 || pipe(c2pSTDERR)<0 || (childpid = fork()) == -1) {  
        perror("Error in initalization.");
        return -1;
    }; 

    if(childpid > 0) {
        int a;
        int b;
        /* Take the input byte by byte and store the characters in a vector,
        this way program is not dependent on any buffer size. */
        char ptr[] = "";
        std::vector<char> vec;

        close(p2c[READ_FD]);         // parent won't read from parent-to-child (only write to it)
        close(c2pSTDOUT[WRITE_FD]);  // parent won't write to child-to-parent STDOUT (only read from it)
        close(c2pSTDERR[WRITE_FD]);  // parent won't write to child-to-parent STDERR (only read from it)

        /* Take two integers from STDIN */
        scanf("%d %d", &a, &b);
        std::string str = std::to_string(a) + " " + std::to_string(b); 

        /* Give the required inputs to the child process */
        if(write(p2c[WRITE_FD], str.c_str(), str.size() + 1) == -1) {
            perror("Error while writing to child.");
            return -1;
        }

        /* Open the outfile */
        std::ofstream outfile;
        outfile.open(output, std::ios_base::app);
        
        /* First check the STDOUT endpoint. It blocks the parent and waits for the child to either write to the STDOUT or
        terminate. If child terminates before writing, it means that it has written to STDERR. Therefore go and check STDERR.
        read() returns 0 if EOF is reached. */
        if(read(c2pSTDOUT[READ_FD], ptr, 1) > 0) { 
            vec.push_back(ptr[0]);
            while(read(c2pSTDOUT[READ_FD], ptr, 1) > 0) vec.push_back(ptr[0]);
            outfile << "SUCCESS:\n";
        }  else {
            if(read(c2pSTDERR[READ_FD], ptr, 1) == -1) {
                perror("Output is neither in STDOUT nor in STDERR.");
                return -1;
            }
            vec.push_back(ptr[0]);
            while(read(c2pSTDERR[READ_FD], ptr, 1) > 0) vec.push_back(ptr[0]);
            outfile << "FAIL:\n";
        }

        std::string str(vec.begin(), vec.end());  // vector to string conversion
        outfile << str;  

        // close the ends of the pipes
        close(p2c[WRITE_FD]);
        close(c2pSTDERR[READ_FD]);
        close(c2pSTDOUT[READ_FD]);

        outfile.close();


    } else { // child process
        dup2(p2c[READ_FD], STDIN_FILENO);            // stdin - read from parent
        dup2(c2pSTDOUT[WRITE_FD], STDOUT_FILENO);    // stdout - write into the parent
        dup2(c2pSTDERR[WRITE_FD], STDERR_FILENO);    // stderr - write into the parent

        /* Close all the file descriptors */
        close(c2pSTDERR[READ_FD]);
        close(c2pSTDERR[WRITE_FD]);
        close(c2pSTDOUT[READ_FD]);
        close(c2pSTDOUT[WRITE_FD]);
        close(p2c[READ_FD]);
        close(p2c[WRITE_FD]);

        // Blackbox either produces an output to stdout or gives error to stderr.
        execl(executable, "./blackbox", NULL);
    }
    return 0;
}