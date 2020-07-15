from project import db


class ObserverService:
    def __init__(self, database):
        self.database = database

    def insert_data(self, data):
        data = self.database(**data)
        db.session.add(data)
        db.session.commit()
