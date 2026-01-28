from flask import render_template, request, jsonify
from app import app, models
import sqlite3
models.cr_d()

def get_db():
    conn = sqlite3.connect("data_b.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT Category FROM products")
        rows = cursor.fetchall()
        categories = [r["Category"] for r in rows if r["Category"] is not None]

        # fetch initial product list (most recent first)
        cursor.execute("SELECT * FROM products ORDER BY id DESC LIMIT 100")
        prod_rows = cursor.fetchall()
        products = []
        for r in prod_rows:
            products.append({
                "id": r["id"],
                "name": r["Pr_name"],
                "price": r["Price"],
                "category": r["Category"],
                "brand": r["Brand"],
                "date": r["Date"],
                "discount": r["Discount"],
                "description": r["DESCRIPTION"] if "DESCRIPTION" in r.keys() else ""
            })
    except Exception:
        categories = []
        products = []
    finally:
        conn.close()
    return render_template("home.html", categories=categories, products=products)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    category = request.form.get("category", "all")
    min_price = request.form.get("min_price", "").strip()
    max_price = request.form.get("max_price", "").strip()

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if query:
        sql += " AND (Pr_name LIKE ? OR Brand LIKE ?)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q])

    if category and category != "all":
        sql += " AND Category = ?"
        params.append(category)
    
    if min_price:
        try:
            float_min = float(min_price)
            sql += " AND CAST(Price AS REAL) >= ?"
            params.append(float_min)
        except ValueError:
            pass

    if max_price:
        try:
            float_max = float(max_price)
            sql += " AND CAST(Price AS REAL) <= ?"
            params.append(float_max)
        except ValueError:
            pass

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    finally:
        conn.close()

    products = []
    for r in rows:
        products.append({
            "id": r["id"],
            "name": r["Pr_name"],
            "price": r["Price"],
            "category": r["Category"],
            "brand": r["Brand"],
            "date": r["Date"],
            "discount": r["Discount"],
            "description": r["DESCRIPTION"] if "DESCRIPTION" in r.keys() else ""
        })

    return jsonify({"products": products})
