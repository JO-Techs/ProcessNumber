import redis
import json
import pika
import time
from celery_app import app

@app.task
def multiply():
    time.sleep(5)
    r = redis.Redis(host='redis', port=6379)
    data = r.get('valid_ints')
    if not data:
        print("Worker: No valid integers")
        return

    valid = json.loads(data)
    result = [x * 10 for x in valid]

    conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    ch = conn.channel()
    ch.queue_declare(queue='processed_list')
    ch.basic_publish(exchange='', routing_key='processed_list', body=json.dumps(result))
    print("Worker: Sent processed list:", result)
    conn.close()
