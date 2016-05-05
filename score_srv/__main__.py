#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import time
import json
import sqlite3
from flask import Flask
from flask import request

DB_NAME = 'scores.db'
app = Flask(__name__)

try:
    with open('secret', 'rb') as f:
        SECRET = f.read()
except:
    raise

@app.route('/')
def index():
    return ''

@app.route('/score', methods=['GET'])
def get_user_score():
    db = sqlite3.connect(DB_NAME)
    db_c = db.cursor()
    scores = []
    for x in db_c.execute("SELECT * FROM scores"):
        scores.append("{date: '%s', username='%s', score=%d}" % (
            x[0], x[1], int(x[2])
        ))
    db.close()
    return json.dumps(scores)

@app.route('/submit', methods=['POST'])
def login():
    if request.method == 'POST':
        # HMAC check
        if request.form['check'] != hashlib.sha512(SECRET + hashlib.sha512(SECRET + request.form['score'].encode('utf-8').hexdigest())).hexdigest():
            return json.dumps("{state: 'KO'}")
        # Check passed, process to score save.
        try:
            db = sqlite3.connect(DB_NAME)
            db_c = db.cursor()
            try:
                db_c.execute('UPDATE scores SET date=?, score=? WHERE username=?', (
                    time.ctime(),
                    int(request.form['score']),
                    request.form['username']
                ))
            except sqlite3.OperationalError as e:
                db_c.execute("INSERT INTO scores VALUES (?, ?, ?)", (
                    time.ctime(),
                    request.form['username'],
                    int(request.form['score'])
                ))
            db.commit()
            db.close()
        except:
            raise
            return json.dumps("{state: 'KO'}")
    return json.dumps("{state: 'OK'}")
    

if __name__ == '__main__':
    try:
        db = sqlite3.connect(DB_NAME)
        db_c = db.cursor()
        db_c.execute('''CREATE TABLE scores (date text, username text, score int, PRIMARY KEY (username))''')
        db.commit()
        db.close()
    except:
        pass

    app.run(host='0.0.0.0', debug=True)

