import os
import psycopg2
from flask import Blueprint, current_app, g
from flask.cli import with_appcontext

# connects to db
def get_db():
    if 'db' not in g:
        DATABASE_URL = os.environ['DATABASE_URL']
        g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
    return g.db

def init_app(app):
    app.teardown_appcontext(close_db)

# closes db
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# creates DB# main stat query
def query(dept, state):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT deptname, cost as total FROM deptCost WHERE deptname = %s ;", (dept,))
    report = cur.fetchone()
    cur.close()
    return report

# item list query
def itemQuery(dept, state):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT item, cost, quantity FROM deptList WHERE deptname = %s AND state = %s;", (dept,state,))
    report = cur.fetchall()
    cur.close()
    db.close()
    return report
 
