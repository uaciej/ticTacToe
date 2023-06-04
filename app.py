from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/ttt'

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()