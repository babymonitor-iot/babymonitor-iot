import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = "sqlite:///" + os.path.join(basedir, "storage.db")


def make_config(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
