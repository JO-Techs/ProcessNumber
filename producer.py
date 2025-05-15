import pika
import json
import time

time.sleep(5)  # Wait for RabbitMQ

for i in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"Connection attempt {i+1} failed, retrying in 3s...")
        time.sleep(3)
else:
    print("Failed to connect to RabbitMQ after 10 attempts")
    exit(1)
    
channel = connection.channel()
channel.queue_declare(queue='raw_list')

data = ["12", "abc", "5", "9.0", "100", "xyz", "30"]
channel.basic_publish(exchange='', routing_key='raw_list', body=json.dumps(data))
print("Producer: Sent data to RabbitMQ")

connection.close()
