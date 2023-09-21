
import pika




def callback(ch, method, properties, body):
    print("Received message:", body)




connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))
channel = connection.channel()
queue_name = 'clicks'
channel.queue_declare(queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
