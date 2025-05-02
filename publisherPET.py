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

def zone_conversion(lat, lon):
    if lat >= 0 and lon >= 0:
        return "Zone A"  
    elif lat >= 0 and lon < 0:
        return "Zone B"  
    elif lat < 0 and lon >= 0:
        return "Zone C"  
    else:
        return "Zone D"  
def id_to_token(userId):
    tokens = ["V-001", "V-002", "V-003", "V-004", "V-005", "V-006", "V-007", "V-008", "V-009", "V-010"]
    return tokens[int(userId) - 1]

def create_message_minimized():
    temperature = 20 + (random.randint(0, 100) * 4)
    severity = random.choice(["low", "medium", "high"])
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    zone = zone_conversion(lat, lon)
    token = id_to_token(str(random.randint(1, 10)))
    msg = f"Severity: {severity}, zone: {zone}, token: {token}"
    return msg


def publish_encrypted(client):
    msg_count = 0
    print("Publishing encrypted messages")
    time.sleep(1)

    msg = create_message()

    encrypted_msg = cipher.encrypt(msg.encode())
    result = client.publish(topic, "Encrypted message: " + str(encrypted_msg))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Sent encrypted `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1

def publish_minimized(client):
    msg_count = 0
    print("Publishing minimized messages")
    time.sleep(1)

    msg = create_message_minimized()


    result = client.publish(topic, "Minimized message: " + str(msg))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Sending  `{msg}` (minimzed) to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1

def publish_encrypted_minimized(client):
    msg_count = 0
    print("Publishing encrypted and minimized messages")
    time.sleep(1)

    msg = create_message_minimized()

    encrypted_msg = cipher.encrypt(msg.encode())
    result = client.publish(topic, "Encrypted and minimized message: " + str(encrypted_msg))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Sent encrypted `{msg}` (minimized) to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    while True:
        input("Press any key to send Encrypted Message")
        publish_encrypted(client)
        input("Press any key to send Minimized Message")
        publish_minimized(client)
        input("Press any key to send Encrypted and Minimized Message")
        publish_encrypted_minimized(client)

run()
