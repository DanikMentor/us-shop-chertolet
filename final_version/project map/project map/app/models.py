import sqlite3

def cr_d():
    conn = sqlite3.connect("data_b.db")
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Login TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Mail TEXT NOT NULL UNIQUE,
        Phone_n TEXT,
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
        Discount TEXT NOT NULL,
        DESCRIPTION TEXT DEFAULT 'No description available.'
    )
    """)

    cursor.execute("SELECT count(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Toyota Camry", "24000", "Sedan", "Toyota", "2022-01-15", "5%", "Otli4naja masina o4en nravitsa moja mama eden na tojote uze mnogo let vrode ese ne slomalas"),
            ("Honda Accord", "26000", "Sedan", "Honda", "2022-03-22", "7%", "Koro4e gemini skazal 4to honda t1 4to u neje o4en krytoi motor a tak ka gemini umnij ja emy very"),
            ("Ford F-150", "30000", "Truck", "Ford", "2021-11-10", "10%", "Ford krytaja masina mne o4en nravitsa pomnu vidos na jutube pro ford smotrel tolko eto bilo davno ja uze ni4ego ne pomnu :(( ))"),
            ("Chevrolet Silverado", "32000", "Truck", "Chevrolet", "2022-02-05", "8%", "OOOO chertole Silverado odna iz samih znamenetih i popularnih masin na saite.Objazatelko k pokupke esli vi javlajetes elitnim predstovitelem chertolet community"),
            ("BMW X5", "60000", "SUV", "BMW", "2022-04-12", "6%", "BMW prikolnijie takije masini esli vi urod kotorij lubit gonat na trasse obsetvenogo polzovanije rekomenduyu k pokupke"),
            ("Audi Q7", "65000", "SUV", "Audi", "2021-12-30", "9%", "Audi — это «технологическое превосходство». Для площадки вроде Chertolet.lv это машины высшего эшелона."),
            ("Mercedes-Benz C-Class", "55000", "Sedan", "Mercedes-Benz", "2022-05-20", "4%", "Prikolnaja masina na kartinke iz gugla vigladit stilno a style eto samij vaznij parametr"),
            ("Nissan Altima", "23000", "Sedan", "Nissan", "2022-03-18", "5%", "Ne stoit pokupat etu masinu ona malo stoit a zna4it ja zarabotaju malo deneg"),
            ("Jeep Grand Cherokee", "40000", "SUV", "Jeep", "2021-10-25", "11%", "Krytoi car kotorij pozvolajiet ehat po griazi. No lutse tak ne delat так как можно сесть на зону :)"),
            ("Ram 1500", "35000", "Truck", "Ram", "2022-01-08", "7%", "Krytoi gruzak mne o4en nravitsa kuzov bolsoi kak raz dla mojego dryga sani")
        ]

        cursor.executemany("""
        INSERT INTO products (Pr_name, Price, Category, Brand, Date, Discount, DESCRIPTION)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_products)
    else:
        print("Всё заебок база есть")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    cr_d()

