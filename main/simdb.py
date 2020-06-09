import pandas as pd
import os.path
import os
import psycopg2
from os import path
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

    report = db.execute(
            'SELECT deptName, cost as total FROM deptCost WHERE deptName = ?', (dept,)).fetchone()
    return report

# item list query
def itemQuery(dept, state):
    db = get_db()
    report = db.execute(
        'SELECT item, cost, quantity FROM deptList WHERE deptName = ? AND state = ? LIMIT 50', (dept, state,)).fetchall()
    return report
 
# crates a Dataframe from the CSV
def loadCSV():
    name = "1033Rec"
    rawData = pd.read_csv(name)
    df = pd.DataFrame()
    df["State"] = rawData.State
    df["Dept"] =  rawData.Station
    df["Cost"] = rawData.Value
    df["Quantity"] = rawData.Quantity
    df["Item"] = rawData.Item
    return df

# Temporary but creates a unique list of departments in Washington
def unique(df):    
    uniqueDept = []
    for dept in df["Dept"]:
       if dept in uniqueDept:
          continue
       else:
           uniqueDept.append(dept)
    return uniqueDept

# cleans up dept name
def sanitize(dept):
    iter = 0
    while dept[iter] != " ":
        iter= iter+1
    dept = dept[:iter]
    return dept

# loads dataframe into database
def loadDB(df):
    db = get_db()
    uniqueDept = unique(df)
    clean = []
    for temp in uniqueDept:
        val = sanitize(temp)
        clean.append(val)
    
    deptCost(df, uniqueDept)

    for index, row in df.iterrows():
        cdpt = row.Dept
        for val in clean:
            if val in cdpt:
                cdpt = val
                
        db.execute(
               'Insert INTO deptList(state, deptName, cost, quantity, item) VALUES(?,?,?,?,?)',
               (row.State, cdpt, row.Cost, row.Quantity, row.Item,))
        db.commit()

def deptCost(df, uniqueList):
    db = get_db()
    deptDict= {}
    for item in uniqueList:
        deptDict.update( {item: 0})

    for index, row in df.iterrows():
        for dept in uniqueList:
            if dept in row.Dept:
                val = deptDict[dept]
                tempC = row.Cost.replace('$', "")
                tempC = tempC.replace(',', "")
                tempQ = int(row.Quantity)
                val = val + (float(tempC))
                deptDict.update({sanitize(dept):val})

    for p, v in deptDict.items():
        db.execute(
                'INSERT INTO deptCost(deptName, cost) VALUES(?,?)',
                (p, v,))
        db.commit()





#if not path.exists('police.db'):
#init_db()

#df = loadCSV()
#loadDB(df)
#uniques = unique(df)

#for dept in uniques:
#   query(dept,"WA")

#report = itemQuery(uniques[1], "wa")
#for page in report:
#    print(page["item"], page["cost"], page["quantity"])


