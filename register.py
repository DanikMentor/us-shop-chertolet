import sqlite3
import os

DB_NAME = "data_b.db"

def add_user_to_db(name, lastname, mail, phone, login, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # проверяем, что не занято
    checks = [
        ("Mail", mail, "❌ Такая почта уже зарегистрирована"),
        ("Phone_n", phone, "❌ Такой телефон уже зарегистрирован"),
        ("Login", login, "❌ Такой логин уже занят"),
    ]

    for field, value, msg in checks:
        cursor.execute(f"SELECT 1 FROM users WHERE {field} = ?", (value,))
        if cursor.fetchone():
            conn.close()
            print(msg)
            return False  # не добавили

    # если всё ок — добавляем
    cursor.execute("""
        INSERT INTO users (Name, Lastname, Mail, Phone_n, Login, Password, Num_i_p, Bonus)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, lastname, mail, phone, login, password, "0", "0"))

    conn.commit()
    conn.close()
    return True


def login_user():
    login = input("Login: ")
    password = input("Password: ")

    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, Name, Lastname FROM users
        WHERE Login = ? AND Password = ?
    """, (login, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Вход выполнен. Добро пожаловать, {user[1]}!")
    else:
        print("❌ Неверный логин или пароль")


def sign_up():
    name = input("Name: ").strip()
    lastname = input("Lastname: ").strip()
    mail = input("Mail: ").strip()
    phone = input("Phone: ").strip()
    login = input("Login: ").strip()
    password = input("Password: ").strip()

    ok = add_user_to_db(name, lastname, mail, phone, login, password)
    if ok:
        print("✅ Пользователь добавлен!")


def del_b():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("🗑 База удалена")
    else:
        print("Базы нет")

def menu():
    while True:
        print("\n1 - Login")
        print("2 - Sign up")
        print("3 - Exit")

        a = input("Choose: ")

        if a == "1":
            login_user()
        elif a == "2":
            sign_up()
        elif a == "3":
            break
        elif a == "4":
            del_b()
        else:
            print("Неверный пункт")


menu()




