from project.model.publisher.smartphone_publisher import SmartphonePublisher
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from time import sleep
from datetime import datetime
from project.model.smartphone import confirm_user
from project import socketio

user_confirm = None
control_thread = None


def check_is_notification(message):
    if message["type"] == "notification":
        return True
    return False


def forward_message_smart_tv():
    SmartphonePublisher("notification").start()


def send_confirm_baby_monitor():
    SmartphonePublisher("confirmation").start()


def check_user_confirm():
    data_send = BabyMonitorService(BabyMonitorSend).last_record()
    data_receive = BabyMonitorService(BabyMonitorReceive).last_record()
    if data_receive:
        if data_receive["id_notification"] == data_send["id"]:
            return True

    return False


def wait_user_confirm(*body):
    global confirm_user

    for _ in range(5):
        sleep(1)
        if confirm_user:
            return None
    if not confirm_user:
        forward_message_smart_tv(body)
        socketio.emit("SmartphoneSent", {"info": "Notification Forward to TV!"})

def type_notification(body):
    if body:
        if not body["breathing"]:
            return (
                f"Emma hasn't been breathing for {body['time_no_breathing']} seconds."
            )

        elif body["crying"]:
            return "Emma is crying."
