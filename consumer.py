import pika
import redis
import json
import time

time.sleep(5)

r = redis.Redis(host='redis', port=6379)

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

def is_valid_integer(s):
    try:
        int(s)
        return True
    except:
        return False

def callback(ch, method, properties, body):
    data = json.loads(body)
    valid = [int(x) for x in data if is_valid_integer(x)]
    r.set('valid_ints', json.dumps(valid))
    print("Consumer: Stored valid integers in Redis:", valid)

channel.basic_consume(queue='raw_list', on_message_callback=callback, auto_ack=True)
print("Consumer: Waiting for messages...")
channel.start_consuming()
