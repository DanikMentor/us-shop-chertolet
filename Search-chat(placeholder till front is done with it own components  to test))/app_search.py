from flask import Flask, render_template, request, jsonify
from database import db, Product, init_sample_data
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initializing database
db.init_app(app)
# Chat responses (placeholder)
CHAT_RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "products": "We offer a wide range of products in Electronics, Furniture, Kitchen, andOffice categories.",
    "price": "Prices range from $9.99 to $999.99. Use the price filter to narrow down your search.",
    "shipping": "Shipping takes 3-5 business days. Free shipping on orders over $50!",
    "contact": "You can contact us at support@example.com or call (555) 123-4567.",
    "hours": "Our support is available Monday-Friday, 9AM-6PM EST.",
    "default": "I'm here to help! You can ask about: products, price, shipping, contact, or hours."
}
@app.before_request
def create_tables():
    db.create_all()
# Add sample data if database is empty
    if Product.query.count() == 0:
        init_sample_data()

@app.route('/')
def index():
    products = Product.query.all()
    # Get unique categories for filter dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    return render_template('index.html',products=products, categories=categories, chat_responses=list(CHAT_RESPONSES.keys()))
@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('query', '').strip()
    selected_category = request.form.get('category', 'all')
    min_price = request.form.get('min_price', '')
    max_price = request.form.get('max_price', '')
    # Start with base query
    query = Product.query
    if search_query:
        query = query.filter(
            Product.name.contains(search_query) |
            Product.description.contains(search_query)
    )
    # Apply category filter
    if selected_category != 'all':
        query = query.filter(Product.category == selected_category)
    # Apply price filters
    if min_price:
        query = query.filter(Product.price >= float(min_price))
    if max_price:
        query = query.filter(Product.price <= float(max_price))
    products = query.all()
    # Convert products to dictionary format for JSON response
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'description': product.description
            })
    return jsonify({'products': products_list})
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower().strip()
    # Simple keyword matching for placeholder responses
    response = CHAT_RESPONSES['default']
    for key in CHAT_RESPONSES:
        if key in user_message:
            response = CHAT_RESPONSES[key]
            break
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)