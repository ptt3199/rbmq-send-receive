import threading
import time
import pika
import json
import requests
from requests.auth import HTTPBasicAuth

class MessageHandler:
    def __init__(self):
        self._handlers = {}

    def register_handler(self, name_exchange, handler):
        self._handlers[name_exchange] = handler

    def handle_message(self, channel, method, properties, body):
        message = json.loads(body.decode())
        print(f"Received message: {message}")
        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)

# Define the exchange and queue names
queue_data = {
    "LANE_VIOLATION_EXCHANGES": "LANE_VIOLATION_QUEUE",
}

class PikaListener:
    def __init__(self, exchange_type):
        self.exchange_type = exchange_type

    def __call__(self, cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.exchange_type = self.__class__.exchange_type

        cls.__init__ = __init__
        cls.exchange_type = self.exchange_type
        return cls

@PikaListener(exchange_type='fanout')
class MQService(object):
    def __init__(self):
        super().__init__()
        self.message_handler = MessageHandler()  # Initialize message_handler
        self._channel = None

    def start_init(self):
        try:
            self.credentials = pika.PlainCredentials('guest', 'guest')
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                                 port=5672,
                                                                                 heartbeat=60,
                                                                                 credentials=self.credentials))
            self._channel = self._connection.channel()
            print(f'Connected pika consumer to localhost:5672')

            for exchange_name, queue_name in queue_data.items():
                print(f"Checking exchange: {exchange_name}, queue: {queue_name}")
                if self.check_if_added(exchange_name, queue_name):
                    print(f"Exchange and queue exist: {exchange_name}, {queue_name}")
                    self._channel.basic_consume(queue=queue_name,
                                                on_message_callback=self.message_handler.handle_message,
                                                auto_ack=False)
                    self.message_handler.register_handler(exchange_name, self.message_handler.handle_message)
                else:
                    print(f"Exchange or queue does not exist: {exchange_name}, {queue_name}")

            print(' [*] Waiting for messages on queue.')
        except Exception as e:
            print("Error: ", e)

    def check_if_added(self, exchange_name, queue_name):
        try:
            # Check if exchange exists
            exchange_url = f'http://localhost:15672/api/exchanges/%2F/{exchange_name}'
            queue_url = f'http://localhost:15672/api/queues/%2F/{queue_name}'
            auth = HTTPBasicAuth('guest', 'guest')

            exchange_response = requests.get(exchange_url, auth=auth)
            queue_response = requests.get(queue_url, auth=auth)

            if exchange_response.status_code == 200 and queue_response.status_code == 200:
                return True
            else:
                print(f"Exchange response status: {exchange_response.status_code}, Queue response status: {queue_response.status_code}")
                return False
        except Exception as e:
            print(f"Error checking if added: {e}")
            return False

    def listen(self):
        while True:
            try:
                self.start_init()
                self._channel.start_consuming()
            except Exception as e:
                print("Error: ", e)
                time.sleep(5)

    def stop(self):
        if self._channel:
            self._channel.stop_consuming()
        if self._connection:
            self._connection.close()

    def __del__(self):
        self.stop()

class StartMQ:
    def __init__(self):
        pass

    @staticmethod
    def init_queue():
        mq_service = MQService()
        mq_service.listen()

    def start(self):
        t = threading.Thread(target=self.init_queue, daemon=True)
        t.start()

if __name__ == '__main__':
    StartMQ().start()
    print("MQ Service started and listening for messages.")
    while True:
        time.sleep(1)  # Keep the main thread alive