from project import app, socketio


if __name__ == "__main__":
    print('Run BabyMonitorSoS \n')
    socketio.run(app)
