import pika
import psycopg2
import os


    
postgres_connection = psycopg2.connect(
    host='your_postgresql_host',
    database='your_database_name',
    user='your_username',
    password='your_password'
)

postgres_cursor = postgres_connection.cursor()


def callback(ch, method, properties, body):



    print("Received message:", body)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))
channel = connection.channel()
queue_name = 'clicks'
channel.queue_declare(queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
