import sqlite3
import os

DB_NAME = "data_b.db"

def add_user_to_db(name, lastname, mail, phone, login, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (Name, Lastname, Mail, Phone_n, Login, Password, Num_i_p, Bonus)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, lastname, mail, phone, login, password, "0", "0"))

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM users")
    print("Users count:", cursor.fetchone()[0])

    conn.close()

def sign_up():
    name = input("Name: ")
    lastname = input("Lastname: ")
    mail = input("Mail: ")
    phone = input("Phone: ")
    login = input("Login: ")
    password = input("Password: ")

    add_user_to_db(name, lastname, mail, phone, login, password)
    print("✅ Пользователь добавлен!")

def del_b():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("🗑 База удалена")
    else:
        print("Базы нет")

def menu():
    print("DB PATH:", os.path.abspath(DB_NAME))
    a = int(input("1-login, 2-sign up, 3-delete base: "))

    if a == 2:
        sign_up()
    elif a == 3:
        del_b()
    else:
        print("Пока логин не реализован")

menu()


