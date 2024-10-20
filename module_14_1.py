import sqlite3

connection = sqlite3.connect('not_telegram.db')
cur = connection.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')
for i in range(1, 11):
    cur.execute(" INSERT INTO Users(username, email, age, balance) VALUES (?,?,?,?)",
                (f"User{i}", f"example{i}@gmail.com", str(i * 10), "1000"))

connection.commit()
connection.close()
