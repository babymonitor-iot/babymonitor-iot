from project.util.construct_scenario import (
    exchange,
    bm_info,
)
from project.util.config_broker import ConfigScenario
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from project.util.generate_data import data_from_baby
from project.util.clean_dict import clean_dict_baby_monitor
from threading import Thread
from project import socketio
import json
from project.util.generate_log import log
import pika
import random
from project.model.publisher.smartphone_publisher import SmartphonePublisher
from datetime import datetime
from project.controller.smartphone_controller import user_confirm


once = True


class BabyMonitorPublisher(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "topic")

    def run(self):
        status = self.generate_status()
        self.publish_info_baby(status)

    def publish_info_baby(self, status):
        global once
        '''if status["type"] == "notification" and once:
            random.seed(datetime.now())
            choice = random.choices([True, False], [0.0, 1.0], k=1)[0]
            if choice:
                user_confirm()
            once = False

        if status["type"] == "status":
            once = True'''

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=bm_info,
            properties=pika.BasicProperties(delivery_mode=2,),
            body=json.dumps(status),
        )
        socketio.emit("BabyMonitorSent", status)
        print("(Publish) BM: ", status)

    def generate_status(self):
        data = self.get_data()
        if data["time_no_breathing"] > 5 or data["crying"]:
            data["type"] = "notification"
        else:
            data["type"] = "status"

        data = clean_dict_baby_monitor(data)
        last_record = clean_dict_baby_monitor(
            BabyMonitorService(BabyMonitorSend).last_record()
        )

        if data != last_record:
            BabyMonitorService(BabyMonitorSend).insert_data(data)
            return data

        if last_record and data["breathing"] is False:
            BabyMonitorService(BabyMonitorSend).update_data(data)
            return data
        return data

    def get_data(self):
        data_send = BabyMonitorService(BabyMonitorSend).last_record()
        data_receive = BabyMonitorService(BabyMonitorReceive).last_record()

        if not data_send:
            return data_from_baby("new_status")

        if data_send["type"] == "notification" and not data_receive:
            return data_from_baby("repeat_status")

        if (
            data_send["type"] == "notification"
            and data_receive["id_notification"] != data_send["id"]
        ):
            return data_from_baby("repeat_status")
        if (
            data_send["type"] == "notification"
            and data_receive["id_notification"] == data_send["id"]
        ):
            return data_from_baby("force_fine")

        return data_from_baby("new_status")
