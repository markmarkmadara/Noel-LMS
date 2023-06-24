import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('CREATE TABLE admin (adname TEXT, password TEXT, city TEXT, pin TEXT)')
conn.close()