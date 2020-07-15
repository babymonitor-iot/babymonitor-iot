from multiprocessing import Process
import threading
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from time import sleep
from project import socketio
from project.model.publisher.smartphone_publisher import SmartphonePublisher


class checkUserConfirm(Process):
    def __init__(self):
        Process.__init__(self)

    def run(self):
        while True:
            if self.need_wait_user():
                for _ in range(5):
                    sleep(1)
                    if self.baby_is_normal():
                        break
                SmartphonePublisher("notification").start()

    def need_wait_user(self):
        last, penultimate = self.get_last_and_penultimate_bm()
        if last and penultimate:
            return self.is_first_notification(last["type"], penultimate["type"])

    def get_last_and_penultimate_bm(self):
        last = BabyMonitorService(BabyMonitorSend).last_record()
        if last:
            penultimate = BabyMonitorService(BabyMonitorSend).penultimate_record()
            return last, penultimate
        return None, None

    def is_first_notification(self, last_type, penultimate_type):
        return last_type == "notification" and penultimate_type == "status"

    def baby_is_normal(self):
        last = BabyMonitorService(BabyMonitorSend).last_record()
        return last["type"] == "status"

    def stop(self):
        raise SystemExit()
