TCP STREAM REDIRCTION
====

this project consist of a server, listening on two ports at the time.
The first port will be use to accept input clients, the second for output clients.

This tool is just going to redirect what is said in every input clients to every output clients.

a bit like if you do something like: 

$> nc -l port1 | nc -l port2

But with multiple clients allowed on each ports.
