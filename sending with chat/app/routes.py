from flask import render_template, request, jsonify
from app import app, models
import sqlite3
models.cr_d()

# Simple chat responses
CHAT_RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "products": "We offer a wide range of products in Electronics, Furniture, Kitchen, and Office categories.",
    "price": "Prices range from low to high. Use the price filter to narrow down your search.",
    "shipping": "Shipping takes 3-5 business days. Free shipping on eligible orders.",
    "contact": "You can contact us at support@example.com or call +371 11 111 111.",
    "hours": "Our support is available Monday-Friday, 9AM-6PM.",
    "default": "I'm here to help! Try: hello, products, price, shipping, contact, hours."
}

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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "") or ""
    user_message = user_message.lower().strip()

    # keyword matching
    response = CHAT_RESPONSES.get("default")
    for key in CHAT_RESPONSES:
        if key != "default" and key in user_message:
            response = CHAT_RESPONSES[key]
            break

    # Return response and available options
    return jsonify({"response": response, "options": list(CHAT_RESPONSES.keys())})
