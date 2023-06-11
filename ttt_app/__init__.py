from flask import Flask
from flask_migrate import Migrate
from .extensions import socketio
from .models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/ttt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ttt'
app.static_folder = 'static'


db.init_app(app)
migrate = Migrate(app, db)
socketio.init_app(app)

from ttt_app import routes
from ttt_app import events