from flask import render_template
from app import app

@app.route('/')
def home():
    # Эта функция ищет home.html в папке templates
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')