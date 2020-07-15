from project.model.smartphone import Smartphone
from project import db


class SmartphoneService():
    def insert_data(self, data):
        data_smartphone = Smartphone(**data)
        db.session.add(data_smartphone)
        db.session.commit()

    def last_record(self):
        return Smartphone.query.order_by(Smartphone.id.desc()).first()
