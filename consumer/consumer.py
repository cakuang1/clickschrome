import pika
import psycopg2
import os






postgres_connection = psycopg2.connect(
    host='postgres:5432',
    database='webtracker',
    user='postgres',
    password=''
)
postgres_cursor = postgres_connection.cursor()


postgres_cursor.execute("""
CREATE TABLE IF NOT EXISTS click_data (
    id SERIAL PRIMARY KEY,
    x INTEGER,
    y INTEGER,
    placeclicked VARCHAR(255),
    timestamp TIMESTAMP
);
""")


def callback(ch, method, properties, body):
    



    print("Received message:", body)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))
channel = connection.channel()
queue_name = 'clicks'
channel.queue_declare(queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
