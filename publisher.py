import random
import time

from cryptography.fernet import Fernet
from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883
topic = "srv/temperature"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


key = b'kWzvKqYp5cDgGEU6c8V7NQd_Z3pH8FVlIQc5fn-1vG4='
cipher = Fernet(key)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
   # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def create_message():
    temperature = 20 + (random.randint(0, 100) * 4)
    severity = random.choice(["low", "medium", "high"])
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    ip = "192.168.1." + str(random.randint(1, 255))
    userId = str(random.randint(1, 1000))
    msg = f"temperature: {temperature}, severity: {severity}, lat: {lat}, lon: {lon}, ip: {ip}, userId: {userId}"
    return msg

def publish(client):
    msg_count = 0
    print("Publishing unencrypted/nonminimized messages")
    while True:
        time.sleep(1)

        msg = create_message()

        # Unencrypted message to be sent
        result = client.publish(topic, "Unencrypted, no data minimized message: " + msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent unencrypted/no minimized `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)




run()
