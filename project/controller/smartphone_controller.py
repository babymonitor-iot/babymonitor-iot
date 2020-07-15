from project import socketio
from project.model.publisher.smartphone_publisher import SmartphonePublisher
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from time import sleep

sp_on = False


@socketio.on("smartphoneConnect")
def smartphone_connect():
    global sp_on
    sp_on = True
    # check_user_confirm = checkUserConfirm()
    subscriber_bm = SmartphoneSubscriber("babymonitor")
    subscriber_tv = SmartphoneSubscriber("smart_tv")
    subscriber_bm.start()
    subscriber_tv.start()
    # check_user_confirm.start()
    while True:
        sleep(1)
        if not sp_on:
            subscriber_bm.stop()
            subscriber_tv.stop()
            # check_user_confirm.stop()
            break


@socketio.on("smartphoneDisconnect")
def smartphone_disconnect():
    global sp_on
    sp_on = False


@socketio.on("confirmUser")
def user_confirm():
    last_send = BabyMonitorService(BabyMonitorSend).last_record()
    id_notification = last_send["id"]
    BabyMonitorService(BabyMonitorReceive).insert_data(
        dict(id_notification=id_notification)
    )
    SmartphonePublisher("confirmation").start()
