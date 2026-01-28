import sqlite3
import os

DB_NAME = "data_b.db"

def add_user_to_db(login, password, mail, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #check
    checks = [
        ("Mail", mail, "❌This mail already signed"),
        ("Phone_n", phone, "❌ This phone already signed"),
        ("Login", login, "❌ This login already signed"),
    ]

    for field, value, msg in checks:
        cursor.execute(f"SELECT 1 FROM users WHERE {field} = ?", (value,))
        if cursor.fetchone():
            conn.close()
            print(msg)
            return False  

    
    cursor.execute("""
        INSERT INTO users (Login, Password, Mail, Phone_n, Num_i_p, Bonus)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (login, password, mail, phone, "0", "0"))


    conn.commit()
    conn.close()
    return True


def add_product_to_db(Pr_name, Price, Category, Brand, Date, Discount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (Pr_name, Price, Category, Brand, Date, Discount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (Pr_name, Price, Category, Brand, Date, Discount))

    conn.commit()
    conn.close()
    return True

def add_product():
    Pr_name = input("Product name: ").strip()
    Price = input("Price: ").strip()
    Category = input("Category: ").strip()
    Brand = input("Brand: ").strip()
    Date = input("Date: ").strip()
    Discount = input("Discount: ").strip()

    ko = add_product_to_db(Pr_name, Price, Category, Brand, Date, Discount)
    if ko:
        print("Product added")



def login_user():
    login = input("Login: ")
    password = input("Password: ")

    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE Login = ? AND Password = ?
    """, (login, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Login completed")
    else:
        print("❌ Incorrect login or password")


def sign_up():
    login = input("Login: ").strip()
    password = input("Password: ").strip()
    mail = input("Mail: ").strip()
    phone = input("Phone: ").strip()

    ok = add_user_to_db(login, password, mail, phone)
    if ok:
        print("✅ User added!")


def del_b():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("🗑Base deleted")
    else:
        print("No base")

def menu():
    while True:
        print("\n1 - Login")
        print("2 - Sign up")
        print("3 - Add_product")
        print("4 - Exit")

        a = input("Choose: ")

        if a == "1":
            login_user()
        elif a == "2":
            sign_up()
        elif a == "3":
            add_product()
        elif a == "4":
            break
        elif a == "5":
            del_b()
        else:
            print("Incorrect number")


menu()