import sqlite3

def cr_d():
    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Login TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Mail TEXT NOT NULL UNIQUE,
        Phone_n TEXT NOT NULL UNIQUE,
        Num_i_p TEXT NOT NULL,
        Bonus INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pr_name TEXT NOT NULL,
        Price TEXT NOT NULL,
        Category TEXT NOT NULL,
        Brand TEXT NOT NULL,
        Date TEXT NOT NULL,
        Discount TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Login TEXT NOT NULL,
        Phone_n TEXT NOT NULL,
        Mail TEXT NOT NULL,
        Delivery TEXT NOT NULL,
        Adress_to_delivery TEXT NOT NULL,
        Payment TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    cr_d()
