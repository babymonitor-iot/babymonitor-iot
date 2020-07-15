from project import socketio
from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from project.model.baby_monitor import BabyMonitorSend
from project.model.service.baby_monitor_service import BabyMonitorService
from time import sleep
from datetime import datetime
from project.util.generate_data import data_from_baby

bm_on = False


@socketio.on("babymonitorConnect")
def babymonitor_connect():
    global bm_on
    bm_on = True
    data = data_from_baby("force_fine")
    data['type'] = 'status'
    BabyMonitorService(BabyMonitorSend).insert_data(data)
    info = {"info": "Baby Monitor Start"}
    socketio.emit("BabyMonitorInformation", info)
    subscriber = BabyMonitorSubscriber()
    subscriber.start()
    while True:
        sleep(1)
        if bm_on:
            publisher = BabyMonitorPublisher()
            publisher.start()
        else:
            subscriber.stop()
            break


@socketio.on("babymonitorDisconnect")
def babymonitor_disconnect():
    global bm_on
    bm_on = False
