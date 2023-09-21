import pika
import psycopg2
import os
import time
import json


# Read PostgreSQL connection details from environment variables
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_port = os.environ.get('POSTGRES_PORT', '5432')
postgres_db = os.environ.get('POSTGRES_DB', 'webtracker')
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_password = os.environ.get('POSTGRES_PASSWORD', '')

# Read RabbitMQ connection details from environment variables
rabbitmq_host = os.environ.get('RABBITMQ_HOST')
rabbitmq_port = os.environ.get('RABBITMQ_PORT')



postgres_connection = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database=postgres_db,
    user=postgres_user,
    password=postgres_password
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
    try:
        decoded_body = json.loads(body)  # Parse the JSON string to a dictionary
        x = decoded_body.get('x')
        y = decoded_body.get('y')
        placeclicked = decoded_body.get('targetElement')
        timestamp = decoded_body.get('timestamp')
        sql = "INSERT INTO click_data (x, y, placeclicked, timestamp) VALUES (%s, %s, %s, %s)"
        values = (x, y, placeclicked, timestamp)
        postgres_cursor.execute(sql, values)
        postgres_connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error inserting data:", str(e))


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host,rabbitmq_port))
    print('connectionmade')
    channel = connection.channel()
    channel.queue_declare(queue='clicks')
    channel.basic_consume(queue='clicks', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()