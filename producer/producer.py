from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)



rabbitmq_queue = 'clicks'

@app.route('/send_click', methods=['POST'])
def send_click():
    try:
        click_data = request.json
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue, durable=False)
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(click_data))
        connection.close()
        return jsonify({'message': 'Click data sent to RabbitMQ'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
