import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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

def get_db():
    con = psycopg2.connect(dbname='pytest', user = 'kd', host = '', password= '')
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return con

def tables():
    con = get_db()
    table = (
            """
            CREATE TABLE deptList(
                recid SERIAL PRIMARY KEY,
                state VARCHAR(255) NOT NULL, 
                deptname VARCHAR(255) NOT NULL, 
                cost VARCHAR(255) NOT NULL, 
                quantity INTEGER NOT NULL, 
                item VARCHAR(255) NOT NULL
                )
            """
            , 
            """
            CREATE TABLE deptCost(
                deptid SERIAL PRIMARY KEY, 
                deptname VARCHAR(255) NOT NULL,
                cost float(4) NOT NULL
                )
            """)
    db = con.cursor()
    for placemat in table:
        db.execute(placemat)
    
    db.close()
    con.commit()


# loads dataframe into database
def loadDB(df):
    conn = get_db()
    db = conn.cursor()
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
               'Insert INTO deptlist(state, deptName, cost, quantity, item) VALUES(%s,%s,%s,%s,%s)',
               (row.State, cdpt, row.Cost, row.Quantity, row.Item))
    conn.commit()
    

def deptCost(df, uniqueList):
    conn = get_db()
    db = conn.cursor()
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
                'INSERT INTO deptcost(deptName, cost) VALUES(%s,%s)',
                (p, v))

    conn.commit()
def testFunc():
    conn =  get_db()
    cur = conn.cursor()
    cur.execute("SELECT * from deptList limit 10")
    report = cur.fetchall()
    for item in report:
        print(item[1])
testFunc()
#tables()
#df = loadCSV()
#loadDB(df)


