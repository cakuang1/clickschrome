from flask import Flask, request, jsonify,render_template
import pika
import json
import os
from flask_cors import CORS
import psycopg2


# Read PostgreSQL connection details from environment variables
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_port = os.environ.get('POSTGRES_PORT', '5432')
postgres_db = os.environ.get('POSTGRES_DB', 'webtracker')
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'password')

# Read RabbitMQ connection details from environment variables
rabbitmq_host = os.environ.get('RABBITMQ_HOST','localhost')
rabbitmq_port = os.environ.get('RABBITMQ_PORT',5672)



postgres_connection = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database=postgres_db,
    user=postgres_user,
    password=postgres_password
)
postgres_cursor = postgres_connection.cursor()


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



@app.route('/heatmap', methods=['GET'])
def generate_heatmap():
    # You can use the data from your database to generate the heatmap data in JavaScript
    # Replace the sample_data with your actual heatmap data
    sample_data = [
        {"x": 100, "y": 200, "value": 5},
        {"x": 150, "y": 250, "value": 8},
        # Add more data points as needed
    ]
    return render_template('heatmap.html', heatmap_data=sample_data)

@app.route('/get_clicks', methods=['GET'])
def test():

    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
