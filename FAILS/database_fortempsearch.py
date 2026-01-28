from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
def __repr__(self):
    return f'<Product {self.name}>'
def init_sample_data():
    """Add sample data to database"""
    sample_products = [
        Product(name='Laptop', category='Electronics', price=999.99, description='High-performance laptop'),
        Product(name='Desk Chair', category='Furniture', price=249.99, description='Ergonomic office chair'),
        Product(name='Coffee Mug', category='Kitchen', price=14.99, description='Ceramic coffee mug'),
        Product(name='Smartphone', category='Electronics', price=799.99, description='Latest smartphone model'),
        Product(name='Bookshelf', category='Furniture', price=149.99, description='Wooden bookshelf'),
        Product(name='Headphones', category='Electronics', price=199.99,
        description='Noise-cancelling headphones'),
        Product(name='Notebook', category='Office', price=9.99, description='Professional notebook'),
        Product(name='Desk Lamp', category='Furniture', price=39.99, description='LED desk lamp'),
    ]
    for product in sample_products:
        db.session.add(product)
        db.session.commit()
