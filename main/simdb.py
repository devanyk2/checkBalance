import os
import psycopg2
import click
from flask import Blueprint, current_app, g
from flask.cli import with_appcontext

# connects to db
def get_db():
    if 'db' not in g:
        DATABASE_URL = os.environ['DATABASE_URL']
        g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
    return g.db


# closes db
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# creates DB
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('init db')

@click.command('load-db')
@with_appcontext
def load_db_command():
    df = loadCSV()
    loadDB(df)
    click.echo('db loaded')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_db_command)

# main stat query
def query(dept, state):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT deptname, cost as total FROM _deptCost WHERE deptname = %s ;", (dept,))
    report = cur.fetchone()
    return report

# item list query
def itemQuery(dept, state):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT item, cost, quantity FROM _deptList WHERE deptname = %s AND state = %s ;", (dept, state,))
    report =  cur.fetchall()
    return report
 

