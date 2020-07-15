from project import socketio


def log(func):
    def wrapper(*arg):
        socketio.emit('Log', arg[1])
        return func(*arg)

    return wrapper
