#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <setjmp.h>
#include <signal.h>

/* Exception handling */
enum Exceptions {
  ERROR_NO_ARGS,
  ERROR_I_DONT_KNOW,
  Exception,
  NB_ERRORS
};  

static char *err_msgs[NB_ERRORS] = {
  "not enough arguments given",
  "i don't know!"
};

#define GET_MSG(x) err_msgs[x]

/**
 * Defining our try catch throw keywords
 */
static jmp_buf recover;
static int exception;

#define try if (setjmp(recover) == 0)
#define catch(x) else if (x == exception || x == Exception)
#define throw(x) exception = x, longjmp(recover, 1)

/* Programm's code */

void function(char **argv) {

    if (argv[1] == NULL)
        throw(ERROR_NO_ARGS);
    else if (!strcmp(argv[1], "except"))
        throw(ERROR_I_DONT_KNOW);
    while (*argv) {
        printf("%s\n", *argv++);
    }
}

int main(int __attribute__((unused)) argc, char *argv[]) {

    try
        function(argv);
    catch(ERROR_NO_ARGS) 
	    printf("%s:%d: %s\n", __FILE__, __LINE__, GET_MSG(ERROR_NO_ARGS));
    catch(Exception)
	    printf("%s:%d: Unknown exception catched\n", __FILE__, __LINE__);

  return 0;
}
