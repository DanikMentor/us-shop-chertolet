import sqlite3
def cr_d():
    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Lastname TEXT NOT NULL,
        Mail TEXT NOT NULL,
        Phone_n TEXT NOT NULL,
        Login TEXT NOT NULL,
        Password TEXT NOT NULL,
        Num_i_p TEXT NOT NULL,
        Bonus TEXT NOT NULL
        
    )
    """)

    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pr_name TEXT NOT NULL,
        Price TEXT NOT NULL,
        Category TEXT NOT NULL,
        Brand TEXT NOT NULL,
        Date TEXT NOT NULL
       
        
    )
    """)

    users = [
        ("","","","","","","",""),
        ("","","","","","","",""),
        ("","","","","","","","")
    ]
    products = [
        ("","","","",""),
        ("","","","",""),
        ("","","","","")
    ]


    try:
        cursor.executemany(
            "INSERT INTO users (Name, Lastname, Mail, Phone_n, Login, Password, Num_i_p, Bonus) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            users
        )
        cursor.executemany(
            "INSERT INTO products (Pr_name, Price, Category, Brand, Date) VALUES (?, ?, ?, ?, ?)",
            products
        )

    except Exception as a:
        print(a)
    conn.commit()
    conn.close()

cr_d()