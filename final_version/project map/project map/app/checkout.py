from enum import Enum
import os
import json
import sqlite3
from flask import request, render_template, redirect, url_for, jsonify, session
from app import app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CANDIDATES = [
    os.path.join(BASE_DIR, "..", "..", "data_b.db"),
    os.path.join(BASE_DIR, "..", "data_b.db"),
    os.path.join(BASE_DIR, "..", "FAILS", "data_b.db"),
    os.path.join(BASE_DIR, "..", "FAILS", "data.db"),
    os.path.join(BASE_DIR, "data_b.db"),
]


def pick_db() -> str:
    for p in DB_CANDIDATES:
        if os.path.exists(p):
            return os.path.abspath(p)
    return os.path.abspath(DB_CANDIDATES[0])


def db_connect(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_orders_table(db_path: str) -> None:
    with db_connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                Login TEXT NOT NULL,
                Phone_n TEXT NOT NULL,
                Mail TEXT NOT NULL,
                Delivery TEXT NOT NULL,
                Adress_to_delivery TEXT,
                Payment TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'confirmed',
                cart_items TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"


class PaymentVariant(str, Enum):
    card = "card"
    bank = "bank"
    cash = "cash"


class DeliveryMethod(str, Enum):
    salon = "get it in salon"
    home = "delivery to home"


def only_digits(value: str) -> str:
    return "".join(ch for ch in (value or "") if ch.isdigit())


def validate_card(card_number: str):
    if not card_number.isdigit():
        return None

    length = len(card_number)

    if card_number.startswith("4") and length in (13, 16):
        return "VISA"

    if length == 16 and (
        51 <= int(card_number[:2]) <= 55
        or 2221 <= int(card_number[:4]) <= 2720
    ):
        return "MASTERCARD"

    if length == 15 and card_number.startswith(("34", "37")):
        return "AMEX"

    return None


def validate_order(data: dict) -> str | None:
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    delivery = data.get("delivery") or ""
    payment = data.get("payment") or ""

    if not name:
        return "Name is required"

    if len(only_digits(phone)) < 7:
        return "Invalid phone number"

    if "@" not in email or "." not in email:
        return "Invalid email"

    if delivery not in (DeliveryMethod.salon.value, DeliveryMethod.home.value):
        return "Invalid delivery method"

    if delivery == DeliveryMethod.home.value:
        if not (data.get("address") or "").strip():
            return "Delivery address is required"

    if payment not in (
        PaymentVariant.card.value,
        PaymentVariant.bank.value,
        PaymentVariant.cash.value,
    ):
        return "Invalid payment method"

    if payment == PaymentVariant.card.value:
        card_digits = only_digits(data.get("card_number") or "")
        if len(card_digits) < 12:
            return "Invalid card number"

        if not validate_card(card_digits):
            return "Unsupported or invalid card type"

        if not (data.get("card_expiry") or "").strip():
            return "Expiry date required"

        if len(only_digits(data.get("card_cvv") or "")) < 3:
            return "Invalid CVV"

    cart = data.get("cart")
    if not isinstance(cart, list) or len(cart) == 0:
        return "Cart is empty"

   
    for name in cart:
        if not isinstance(name, str) or not name.strip():
            return "Cart item must be a non-empty name"

    return None


def load_user_from_db(db_path: str):
    user_id = session.get("user_id")
    if not user_id:
        return None

    try:
        with db_connect(db_path) as conn:
            row = conn.execute(
                "SELECT Login, Mail, Phone_n FROM users WHERE id=? LIMIT 1",
                (user_id,),
            ).fetchone()
            if not row:
                return None
            return {
                "Login": row["Login"],
                "Mail": row["Mail"],
                "Phone_n": row["Phone_n"],
            }
    except Exception:
        return None


@app.before_request
def setup_tables():
    db = pick_db()
    ensure_orders_table(db)


@app.route("/checkout", endpoint="checkout_page")
@app.route("/checkout.html", endpoint="checkout_page_html")
def checkout():
    """
    Checkout page.
    Works both for logged-in users (pre-fills fields)
    and guests (empty fields).
    """
    db = pick_db()
    user = load_user_from_db(db)
    return render_template("checkout.html", user=user)


@app.route("/api/orders", methods=["GET", "POST"])
def orders_api():
    db = pick_db()

    if request.method == "GET":
        with db_connect(db) as conn:
            rows = conn.execute(
                """
                SELECT id, user_id, Login, Phone_n, Mail, Delivery,
                       Adress_to_delivery, Payment, status, cart_items, created_at
                FROM orders
                ORDER BY id DESC
                """
            ).fetchall()

        result = []
        for row in rows:
            result.append(
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "Login": row["Login"],
                    "Phone_n": row["Phone_n"],
                    "Mail": row["Mail"],
                    "Delivery": row["Delivery"],
                    "Adress_to_delivery": row["Adress_to_delivery"],
                    "Payment": row["Payment"],
                    "status": row["status"],
                    "cart": json.loads(row["cart_items"]) if row["cart_items"] else [],
                    "created_at": row["created_at"],
                }
            )
        return jsonify(result)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    error = validate_order(data)
    if error:
        return jsonify({"error": error}), 400

    user_id = session.get("user_id")

    with db_connect(db) as conn:
        cursor = conn.execute(
            """
            INSERT INTO orders (user_id, Login, Phone_n, Mail, Delivery,
                                Adress_to_delivery, Payment, status, cart_items)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                data.get("name"),
                data.get("phone"),
                data.get("email"),
                data.get("delivery"),
                data.get("address") if data.get("delivery") == DeliveryMethod.home.value else None,
                data.get("payment"),
                OrderStatus.confirmed.value,
                json.dumps(data.get("cart", []), ensure_ascii=False),
            ),
        )
        order_id = cursor.lastrowid

        row = conn.execute(
            """
            SELECT id, user_id, Login, Phone_n, Mail, Delivery,
                   Adress_to_delivery, Payment, status, cart_items, created_at
            FROM orders WHERE id=?
            """,
            (order_id,),
        ).fetchone()

    return (
        jsonify(
            {
                "message": "Order created",
                "order": {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "Login": row["Login"],
                    "Phone_n": row["Phone_n"],
                    "Mail": row["Mail"],
                    "Delivery": row["Delivery"],
                    "Adress_to_delivery": row["Adress_to_delivery"],
                    "Payment": row["Payment"],
                    "status": row["status"],
                    "cart": json.loads(row["cart_items"]) if row["cart_items"] else [],
                    "created_at": row["created_at"],
                },
            }
        ),
        201,
    )
