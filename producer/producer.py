from flask import Flask, request, jsonify
import pika
import json
import os
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
# Read RabbitMQ connection details from environment variables
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.environ.get('RABBITMQ_PORT', '5672')
rabbitmq_queue = 'clicks'


@app.route('/send_click', methods=['POST'])
def send_click():
    try:
        click_data = request.json
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host,rabbitmq_port))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue, durable=False)
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(click_data))
        connection.close()
        return jsonify({'message': 'Click data sent to RabbitMQ'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/test', methods=['GET'])
def test():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
