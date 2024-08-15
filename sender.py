import typer
from pika_publisher import pika_publisher
import json 

app = typer.Typer()


@app.command()
def setup(
  username: str = "guest", 
  password: str = "guest",
  host: str = "localhost",
  port : int = 5672
):
    print(f"Setting up RabbitMQ connection with {username}:{password}@{host}:{port}")
    pika_publisher.__init__(username, password, host, port)
    print("Setup complete")

@app.command()
def send(data: str, exchange_name: str):
    data = json.loads(data)
    print(f"Sending message to exchange {exchange_name}")
    pika_publisher.send_to_rbmq(data, exchange_name)
    print("Message sent")

if __name__ == "__main__":
    app()