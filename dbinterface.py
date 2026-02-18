import json
import sqlite3
import os
import pickle
report = [1,2,3]
name = 'Hi'
dsharpe = 0.5
rsharpe = 0.7
alpha = []

def writeAlpha(name,dsharpe,rsharpe,report,alpha):
	conn = sqlite3.connect('alphaDB.db')
	cur = conn.cursor()

	cur.execute('''
	CREATE TABLE IF NOT EXISTS "alphadb" (
	    "ID"        INTEGER NOT NULL UNIQUE,
	    "Name"      TEXT,
	    "D-Sharpe"  REAL,
	    "R-Sharpe"  REAL,
	    "Report"    TEXT,
	    PRIMARY KEY("ID" AUTOINCREMENT)
	)
	''')

	cur.execute('''
	INSERT INTO alphadb ("Name", "D-Sharpe", "R-Sharpe", "Report")
	VALUES (?, ?, ?, ?)
	''', (name, dsharpe, rsharpe, json.dumps(report)))
	conn.commit()
	last_id = cur.lastrowid
	os.makedirs('alphaBin', exist_ok=True)

	filename = os.path.join('alphaBin', f"{last_id}.pkl")
	with open(filename, "wb") as f:
		pickle.dump(alpha, f)

	cur.close()
	conn.close()

def read_alpha_and_entry(idx):

	filename = os.path.join('alphaBin', f'{idx}.pkl')
	with open(filename, 'rb') as f:
		alpha = pickle.load(f)
	conn = sqlite3.connect('alphaDB.db')
	cur = conn.cursor()
	cur.execute('SELECT * FROM alphadb WHERE ID = ?', (idx,))
	row = cur.fetchone()
	cur.close()
	conn.close()
	return alpha, row