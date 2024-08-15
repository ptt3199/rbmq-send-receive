import pika
import json


class PikaPublisher:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PikaPublisher, cls).__new__(cls)
        return cls.instance

    def __init__(self, username='guest', password='guest', host='localhost', port=5672):
        if not hasattr(self, 'initialized'):  # To prevent reinitialization
            self.username = username
            self.password = password
            self.host = host
            self.port = port
            self.initialized = True

    def startD(self, exchange_name, exchange_type):
        self.credentials = pika.PlainCredentials(
            self.username, self.password
        )
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=self.credentials,
            )
        )
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type
        )
        self._exchange_name = exchange_name

    def send_message(self, data, exchange_name=None):
        try:
            if not exchange_name:
                exchange_name = self._exchange_name
            message = json.dumps(data)
            self._channel.basic_publish(
                exchange=exchange_name, routing_key="", body=message
            )
        except Exception as e:
            print("Error occurred while sending message: %s" + str(e))

    def close(self):
        self._connection.close()

    def send_to_rbmq(self, data, exchange_name):
        try:
            # if not self._connection.is_open:
            #     print("Connection is closed, reconnecting...")
            self.startD(exchange_name=exchange_name, exchange_type="fanout")
            self.send_message(data=data, exchange_name=exchange_name)
            self.close()
            print(f"Send rabbitmq: {data}")
        except Exception as e:
            print("Error occurred while sending message: %s" + str(e))


pika_publisher = PikaPublisher()
