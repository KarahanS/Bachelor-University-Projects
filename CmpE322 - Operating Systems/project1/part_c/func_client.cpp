/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "func.h"

void
func_prog_1(char* output, char *host, char *executable, int number1, int number2)
{
	CLIENT *clnt;
	char * *result_1;
	S  func_1_arg;

#ifndef	DEBUG
	clnt = clnt_create (host, FUNC_PROG, FUNC_VERS, "udp");
	if (clnt == NULL) {
		clnt_pcreateerror (host);
		exit (1);
	}
#endif	/* DEBUG */
	func_1_arg.a = number1;
	func_1_arg.b = number2;
	func_1_arg.c = executable;
	
	result_1 = func_1(&func_1_arg, clnt);
	if (result_1 == (char **) NULL) {
		clnt_perror (clnt, "call failed");
	} else {
		FILE *file;
		file = fopen(output, "a+");
		fputs(*result_1, file);
		fclose(file);
		delete [](*result_1);
	}
#ifndef	DEBUG
	clnt_destroy (clnt);
#endif	 /* DEBUG */
}



int
main (int argc, char *argv[])
{
	if (argc < 4) {
		printf ("usage: %s executable_path output_path server_host\n", argv[0]);
		exit (1);
	}
	// command = argv[0]
	char* executable = argv[1];
	char* output = argv[2];
	char* host = argv[3];

	int a;
	int b;
	scanf("%d %d", &a, &b);

	// call the function with host, executable path and numbers
	func_prog_1 (output, host, executable, a, b);
exit (0);
}
