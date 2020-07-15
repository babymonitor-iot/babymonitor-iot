from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import make_config
from flask_cors import CORS
from flask_babel import Babel
import os
import eventlet
eventlet.monkey_patch()

try:
    os.remove("storage.db")
except Exception:
    pass

app = Flask(__name__)
make_config(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, async_mode='eventlet')
babel = Babel(app)
CORS(app)

from .util import (
    body_message,
    config_broker,
    connection_broker,
    construct_scenario,
)
from .controller import main_controller
from .model import baby_monitor, smartphone, smart_tv
from .solution import observer_model

db.create_all()
