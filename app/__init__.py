from flask import Flask

app = Flask(__name__)

# Сюда потом добавим настройки базы данных (SQLAlchemy)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Очень важно: импортируем routes (маршруты) В КОНЦЕ файла,
# чтобы избежать круговой ошибки (circular import)
from app import routes