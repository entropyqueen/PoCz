#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <setjmp.h>
#include <signal.h>

static jmp_buf recover;
static int exception;

void abort_handler(int __attribute__((unused)) sig) {
  longjmp(recover, 1);
}

/* try catch macro */
#define try(x, y) signal(SIGABRT, &abort_handler), (setjmp(recover) == 0) ? x : y

/* throw macro */
#define throw(x, y) ((x) != 0) ? exception = y, kill(getpid(), SIGABRT) : 0


/* Exception handling */
enum Exceptions {
  ERROR_NO_ARGS,
  ERROR_I_DONT_KNOW,
  NB_ERRORS
};

static char *err_msgs[NB_ERRORS] = {
  "not enough arguments given",
  "i don't know!"
};

#define GET_MSG(x) err_msgs[x]


/* Programm's code */

void function(char **argv) {

  /* If condition is true, we throw with the given message */
  throw(argv[1] == NULL,  ERROR_NO_ARGS);
  throw(!strcmp(argv[1], "except"), 42);

  while (*argv) {
    printf("%s\n", *argv++);
  }
}

int main(int __attribute__((unused)) argc, char *argv[]) {

  try(({
	function(argv);
      }),
    ({
      /* catch */
      if (exception == ERROR_NO_ARGS)
	printf("%s:%d: %s\n", __FILE__, __LINE__, GET_MSG(ERROR_NO_ARGS));
      else
	printf("%s:%d: Unknown exception catched\n", __FILE__, __LINE__);
    }));

  return 0;
}
