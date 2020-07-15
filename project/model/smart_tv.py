from project import db

block = False


class SmartTv(db.Model):
    __tablename__ = "smart_tv"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    block = db.Column(db.Boolean, nullable=True)
