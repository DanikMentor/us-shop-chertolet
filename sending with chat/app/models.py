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
        Date TEXT NOT NULL,
        Discount TEXT NOT NULL,
        DESCRIPTION TEXT DEFAULT 'No description available.'
    )
    """)

    conn.commit()
    conn.close()
    #generate sample data of products(cars)
    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()
    sample_products =  [
        ("Toyota Camry", "24000", "Sedan", "Toyota", "2022-01-15", "5%"),
        ("Honda Accord", "26000", "Sedan", "Honda", "2022-03-22", "7%"),
        ("Ford F-150", "30000", "Truck", "Ford", "2021-11-10", "10%"),
        ("Chevrolet Silverado", "32000", "Truck", "Chevrolet", "2022-02-05", "8%"),
        ("BMW X5", "60000", "SUV", "BMW", "2022-04-12", "6%"),
        ("Audi Q7", "65000", "SUV", "Audi", "2021-12-30", "9%"),
        ("Mercedes-Benz C-Class", "55000", "Sedan", "Mercedes-Benz", "2022-05-20", "4%"),
        ("Nissan Altima", "23000", "Sedan", "Nissan", "2022-03-18", "5%"),
        ("Jeep Grand Cherokee", "40000", "SUV", "Jeep", "2021-10-25", "11%"),
        ("Ram 1500", "35000", "Truck", "Ram", "2022-01-08", "7%")
    ]

    cursor.executemany("""
    INSERT INTO products (Pr_name, Price, Category, Brand, Date, Discount)
    VALUES (?, ?, ?, ?, ?, ?)
    """, sample_products)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    cr_d()

