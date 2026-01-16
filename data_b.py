# data_b.py
import sqlite3

def cr_d():
    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    cr_d()
