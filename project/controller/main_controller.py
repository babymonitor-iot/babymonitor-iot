from project import app
from flask import render_template
from project.controller.baby_monitor_controller import (
    babymonitor_connect,
    babymonitor_disconnect,
)
from project.controller.smartphone_controller import (
    smartphone_connect,
    smartphone_disconnect,
    user_confirm,
)
from project.controller.smart_tv_controller import (
    tv_connect,
    tv_disconnect,
    block_tv,
)
from project.solution.observer_controller import (
    observer_connect,
    observer_disconnect,
)
from project.util.connection_broker import Connection
from project.util.construct_scenario import (
    queue_baby_monitor,
    queue_smart_tv,
    queue_smartphone_bm,
    queue_smartphone_st,
)
from time import sleep
from project import socketio
# from project.util.wait_user_confirm import checkUserConfirm


@app.route("/", methods=["GET"])
def index():
    start_controllers()
    return render_template("index.html")


@socketio.on("restart")
def restart():
    babymonitor_disconnect()
    smartphone_disconnect()
    tv_disconnect()
    observer_disconnect()
    connection = Connection()
    connection.channel.queue_delete(queue=queue_baby_monitor)
    connection.channel.queue_delete(queue=queue_smartphone_bm)
    connection.channel.queue_delete(queue=queue_smartphone_st)
    connection.channel.queue_delete(queue=queue_smart_tv)
    sleep(1)


def start_controllers():
    babymonitor_connect
    babymonitor_disconnect
    smartphone_connect
    smartphone_disconnect
    user_confirm
    tv_connect
    tv_disconnect
    block_tv
    observer_connect
    observer_disconnect
