import cleverbot3
from termcolor import colored, cprint
import sys, time

if len(sys.argv) < 2:
    print ("please give me the first word")
    exit()

b1 = cleverbot3.Cleverbot()
b2 = cleverbot3.Cleverbot()

first = sys.argv[1]

resp1 = b1.ask(first)
cprint("Bot2 : "+ first, 'green', attrs=['bold'], file=sys.stderr)
cprint("Bot1 : " + resp1, 'cyan', attrs=['bold'], file=sys.stderr)

while True:
    resp2 = b2.ask(resp1)
    cprint("Bot2 : " + resp2, 'green', attrs=['bold'], file=sys.stdout)
    time.sleep(1)
    resp1 = b1.ask(resp2)
    cprint("Bot1 : " + resp1, 'cyan', attrs=['bold'], file=sys.stdout)

