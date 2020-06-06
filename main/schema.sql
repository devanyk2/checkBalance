DROP TABLE IF EXISTS deptList;
DROP TABLE IF EXISTS deptCost;

CREATE TABLE deptList(
	recId INTEGER PRIMARY KEY AUTOINCREMENT,
	state STRING NOT NULL, 
	deptName STRING NOT NULL,
	cost REAL NOT NULL,
	quantity INTEGER NOT NULL,
	item STRING NOT NULL
);

CREATE TABLE deptCost(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	deptName STRING NOT NULL,
	cost REAL NOT NULL
)