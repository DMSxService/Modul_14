import sqlite3


def initiate_db():
    connection = sqlite3.connect('product_base2.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INT NOT NULL,
        balance INT NOT NULL
        )
        ''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('product_base2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products


def add_user(username, email, age):
    connection = sqlite3.connect('product_base2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users")
    user_id = cursor.fetchone()[0]    
    cursor.execute(f'''
    INSERT INTO Users VALUES('{user_id+1}','{username}','{email}','{age}', 1000)
    ''')
    connection.commit()
    connection.close()


def is_include(username):
    connection = sqlite3.connect('product_base2.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchone() is None:
        connection.commit()
        connection.close()
        return False
    connection.commit()
    connection.close()
    return True



