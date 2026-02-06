import os
import sqlite3
import pytest
from app import app, models


DB_PATH = "data_b.db"

def setup_module(module):
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        models.cr_d()
    except Exception as e:
        print(f"Error setting up test database: {e}")
    
def test_routes():
    assert app is not None
    routes={rule.rule for rule in app.url_map.iter_rules()}
    assert "/" in routes
    assert "/register" in routes
    assert "/chat" in routes
    assert "/search" in routes

def test_if_db_created():
    assert os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    assert count >0
    cursor.close()
    conn.close()

def test_search_returns_results_without_filters():
    client = app.test_client()
    resp = client.post("/search", data={})
    assert resp.status_code == 200
    assert resp.is_json
    data = resp.get_json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) >= 10

def test_search_query_matches_product_name():
    client = app.test_client()
    resp = client.post("/search", data={"query": "Toyota"})
    assert resp.status_code == 200
    data = resp.get_json()
    products = data.get("products", [])
    assert any("Toyota" in p.get("name", "") for p in products)

def test_search_with_filters():
    client = app.test_client()
    resp = client.post("/search", data={"category": "SUV"})
    assert resp.status_code == 200
    data = resp.get_json()
    products = data.get("products", [])
    assert len(products) >= 1
    for p in products:
        assert p.get("category") == "SUV"

def test_search_price_filters():
    client = app.test_client()
    resp = client.post("/search", data={"min_price": "30000", "max_price": "60000"})
    assert resp.status_code == 200
    data = resp.get_json()
    products = data.get("products", [])
    assert len(products) >= 1
    for p in products:
        price = float(p.get("price", 0))
        assert 30000 <= price <= 60000


def test_chat_default_and_keyword_responses():
    client = app.test_client()

    #default
    resp = client.post("/chat", json={})
    assert resp.status_code == 200
    assert resp.is_json
    data = resp.get_json()
    assert "response" in data and "options" in data
    assert isinstance(data["options"], list)
    assert isinstance(data["response"], str)
    assert "I'm here to help" in data["response"] or data["response"] != ""

    #'hello'
    resp2 = client.post("/chat", json={"message": "hello"})
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert "Hello" in data2.get("response", "") or "hello" in data2.get("response", "").lower()

def test_chat_options_include_expected_keys():
    client = app.test_client()
    resp = client.post("/chat", json={"message": ""})
    data = resp.get_json()
    options = set(data.get("options", []))
    expected = {"hello", "products", "price", "shipping", "contact", "hours", "default"}
    assert expected.issubset(options)

def teardown_module(module):
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
    except Exception as e:
        print(f"Error tearing down test database: {e}")

if __name__ == "__main__":
    pytest.main()


