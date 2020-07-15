from project import db
from threading import Semaphore


control = True
confirm_user = False
mutex_confirm = Semaphore()


class Smartphone(db.Model):
    __tablename__ = "smartphone"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)

