import paho.mqtt.client as mqtt
import json

def create_client(broker="localhost", port=1883):
    client = mqtt.Client()
    client.connect(broker, port, 60)
    return client

def publish_data(topic_prefix, client, data):
    topic = f"{topic_prefix}/data"
    payload = json.dumps(data)
    result = client.publish(topic, payload)
    result.wait_for_publish()