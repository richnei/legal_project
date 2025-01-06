import pika
from decouple import config

RABBITMQ_HOST = config("RABBITMQ_HOST")
RABBITMQ_PORT = config("RABBITMQ_PORT")
RABBITMQ_USER = config("RABBITMQ_USER")
RABBITMQ_PASS = config("RABBITMQ_PASS")
RABBITMQ_QUEUE = config("RABBITMQ_QUEUE")

def get_rabbitmq_channel():
    """Cria e retorna uma conexão e canal do RabbitMQ.

    Returns:
        tuple: Conexão e canal configurados.
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=int(RABBITMQ_PORT),
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    return channel, connection
