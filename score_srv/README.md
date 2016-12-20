# SCORE SERVER

Just a simple REST server for registering scores in a SQLite3 database.

## Routes

```
GET /score
```

Returns the registered scores in json format.

```
POST /submit
```

Submit a score. This takes 3 parameters:
* username: which will be the username to register the score
* score: the score  obtained
* check: a HMAC (using SHA512) of the SECRET value and the score value

## Set Up

In order to set this server up, you'll have to create a 'secret' file wich will contain the SECRET for the HMAC computation, in raw data.

You can then launch the server with python.

