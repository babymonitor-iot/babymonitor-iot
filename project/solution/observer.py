import pika
import threading
import json
from time import sleep
from pyrabbit.api import Client
from project.solution.observer_service import ObserverService
from project.solution.observer_model import ObserverModel
from project import socketio


class Observer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.queue = "observer"
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)
        self.adaptation = False
        self.steps_to_adapt = None
        self.steps_for_behave_normal = None
        self.messages_types = None
        self.exceptional_scenarios = None
        self.subscribe_in_all_queues()

    def get_bindings(self):
        client = Client("localhost:15672", "guest", "guest")
        bindings = client.get_bindings()
        bindings_result = []

        for b in bindings:
            if b["source"] == "exchange_baby_monitor":
                bindings_result.append(b)

        print('BINDINGS: ', bindings_result)
        return bindings_result

    def subscribe_in_all_queues(self):
        bindings = self.get_bindings()

        for bind in bindings:
            self.channel.queue_bind(
                exchange=bind["source"],
                queue=self.queue,
                routing_key=bind["routing_key"],
            )

        return bindings

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(
            " [OBSERVER] Receive: %r Data: %r" % (method.routing_key, body)
        )
        body = json.loads(body.decode("UTF-8"))
        if body['type'] in self.messages_types:
            self.read_message(body, method.routing_key)

    def define_messages(self, types: list):
        self.messages_types = types

    def run(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=False
        )

        self.channel.start_consuming()

    def stop(self):
        print('Entrei aqui')
        raise SystemExit()

    def read_message(self, message, source):
        # Momento opcional para saber se a adaptação falou
        # Acho que isso tá no esganando amiga!
        if message["type"] == "notification":
            print("OBSERVER - Recebi mensagem de notificação")
            if self.adaptation:
                print("OBSERVER - Minha adaptação falhou")
                ObserverService(ObserverModel).insert_data({"success": False})

        # Momento de voltar ao normal
        if message["type"] == "confirmation":
            if self.adaptation:
                print("OBSERVER - Minha adaptação deu certo")
                ObserverService(ObserverModel).insert_data({"success": True})
                self.adaptation = False
                self.return_normal_behave()

        # Momento da adaptação
        if message["type"] == "status" and source == "st_info" and message["block"]:
            print("OBSERVER - Vou desbloquear a TV")
            self.adaptation = True
            self.adaptation_action()

    def adaptation_action(self):
        for function, params in self.steps_to_adapt:
            function(*params)
        sleep(1)
        socketio.emit('successAdapter')

    def return_normal_behave(self):
        for function, params in self.steps_for_behave_normal:
            function(*params)

