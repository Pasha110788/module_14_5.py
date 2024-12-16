import sqlite3


def initiate_db():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL    
        )
        ''')
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS Users(
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           email TEXT NOT NULL,
           age INTEGER NOT NULL,
           balance INTEGER NOT NULL
           )
           ''')
    connection.commit()


def add_user(username, email, age):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)", (username, email, age, 1000))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    c_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    if c_user is None:
        return False
    connection.commit()
    return True


def get_all_products():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM Products").fetchall()
    connection.commit()
    connection.close()
    return products


def add_product(id, title, description, price):
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()
    check_product = cursor.execute("SELECT * FROM Products WHERE id=?", (id,))

    if check_product.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products VALUES(
        '{id}', '{title}', '{description}', '{price}')
''')
    connection.commit()


initiate_db()
add_product(1, 'Набор А', 'Подходит для энергии', 400)
add_product(2, 'Набор Б', "Подходит для силы", 500)
add_product(3, 'Набор В', "Подходит для диеты", 600)
add_product(4, 'Набор Г', 'Подходит для зрения', 200)

add_user('Pasha', 'bodzin1988@gmail.com', 36)
add_user('Nina', 'nina1904@gmail.com', 34)
add_user('Alex', 'alex2345@gmail.com', 23)
add_user('Max', 'max98788@gmail.com', 29)
