from project.model.smart_tv import SmartTv
from project import db


class SmartTvService():
    def insert_data(self, data):
        data = SmartTv(**data)
        db.session.add(data)
        db.session.commit()

    def last_record(self):
        data = SmartTv().query.order_by(
            SmartTv.id.desc()).first()
        if not data:
            return data

        return data.__dict__
