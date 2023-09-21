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
    try:
        x = body.get('x')
        y = body.get('y')
        placeclicked = body.get('targetElement')
        timestamp = body.get('timestamp')
        sql = "INSERT INTO click_data (x, y, placeclicked, timestamp) VALUES (%s, %s, %s, %s)"
        values = (x, y, placeclicked, timestamp)
        postgres_cursor.execute(sql, values)
        postgres_connection.commit()  
        print("Data inserted successfully.")
    except Exception as e:
        print("Error inserting data:", str(e))



connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
channel = connection.channel()
queue_name = 'clicks'
channel.queue_declare(queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
