from project import db
from datetime import datetime


class ObserverModel(db.Model):
    __tablename__ = "observer"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    success = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
