from project.util.construct_scenario import (
    exchange,
    bm_msg,
    st_msg,
)
from project.util.config_broker import ConfigScenario
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from threading import Thread
from project import socketio
import json
import pika


class SmartphonePublisher(ConfigScenario, Thread):
    def __init__(self, type):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "topic")
        self.type = type

    def run(self):
        if self.type == "confirmation":
            self.publish_confirmation()
        if self.type == "notification":
            self.forward_message()

    def publish_confirmation(self):
        confirmation = {"type": "confirmation", "msg": "Notificaiton confirmed!"}

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=bm_msg,
            properties=pika.BasicProperties(delivery_mode=2,),
            body=json.dumps(confirmation),
        )
        socketio.emit("SmartphoneSent", confirmation)
        last_record = BabyMonitorService(BabyMonitorSend).last_record()
        user_confirm = {"id_notification": last_record["id"], "type": "confirm"}
        BabyMonitorService(BabyMonitorReceive).insert_data(user_confirm)

        print("(Publish) SM|BM: ")

    def forward_message(self):
        last_record = BabyMonitorService(BabyMonitorSend).last_record()
        notification = self.format_notification(last_record)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=st_msg,
            properties=pika.BasicProperties(delivery_mode=2,),
            body=json.dumps(notification),
        )
        socketio.emit("SmartphoneSent", notification)
        print("(Publish) SM|ST: ", notification)

    def format_notification(self, body):
        if body:
            if not body["breathing"]:
                msg = f"Emma hasn't been breathing for {body['time_no_breathing']} seconds."
                return {"type": "notification", "msg": msg}

            elif body["crying"]:
                msg = "Emma is crying."
                return {"type": "notification", "msg": msg}
