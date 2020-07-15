from project import socketio
from project.solution.observer import Observer
from project.controller.smart_tv_controller import block_tv

ob_on = False


@socketio.on("observerConnect")
def observer_connect():
    global ob_on
    observer = Observer()
    observer.messages_types = ("status", "notification", "confirmation")
    observer.steps_to_adapt = [(block_tv, (False,))]
    observer.steps_for_behave_normal = [(block_tv, (True,))]
    observer.start()
    while True:
        if not ob_on:
            observer.stop()
            break


@socketio.on("observerDisconnect")
def observer_disconnect():
    global ob_on
    ob_on = False
    print("Observer close connection!")
