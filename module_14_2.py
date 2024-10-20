import sqlite3

connection = sqlite3.connect('not_telegram2.db')
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

for i in range(1, 11, 2):
    cur.execute("UPDATE Users SET balance = ? WHERE username = ?", (500, f"User{i}"))

for i in range(1, 11, 3):
    cur.execute("DELETE FROM Users WHERE username = ?", (f"User{i}",))

cur.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cur.fetchall()
for user in users:
    print(user)


cur.execute("DELETE FROM Users WHERE id = ?", ("6",))
cur.execute("SELECT COUNT(*) FROM Users")
total_users = cur.fetchone()[0]
cur.execute("SELECT SUM(balance) FROM Users")
all_balances = cur.fetchone()[0]
print(all_balances/total_users)

connection.commit()
connection.close()
