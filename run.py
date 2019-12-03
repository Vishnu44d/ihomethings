import paho.mqtt.client as mqtt
import sys
import random
import json
import time
from sensors import read_temperature

def on_connect(client, userdata, flags, rc):    
    print("Result from connect: {}".format(
            mqtt.connack_string(rc)))    
# Subscribe to the senors/alitmeter/1 topic filter 
    client.subscribe("sensors/thermometer/1")
    print("sub 1")
    client.subscribe("sensors/thermometer/1/cmd")  
    print("sub 2")


def on_subscribe(client, userdata, mid, granted_qos):    
    print("I've subscribed")



def on_message(client, userdata, msg):   
    print("Message received. Topic: {}. Payload: {}".format(
            msg.topic, str(msg.payload)))
    if msg.topic == "sesnsors/thermometer/1/cmd":
        print("I recived a new cmd")

def on_disconnect(client, userdata, rc):
    print("Reconnecting")
    client.connect(host="ihomev.duckdns.org", port=1883)

# def publish_data():
#     rc =1
#     while rc != 0:
#         json_body = [
#             {
#                 "measurement": "temperature",
#                 "tags": {
#                     "host": "server01"
#                 },
#                 "fields": {
#                     "value": random.randint(30,60),
#                 }
#             }
#         ]
#         rc, _ = client.publish("sensors/thermometer/1", json.dumps(json_body)).wait_for_publish()
#         print(f"published data {json_body}!")
#         time.sleep(random.randint(2,5))



if __name__ == "__main__":    
    client = mqtt.Client(protocol=mqtt.MQTTv311)    
    client.on_connect = on_connect    
    client.on_subscribe = on_subscribe    
    client.on_message = on_message    
    client.on_disconnect = on_disconnect
    client.connect(host="ihomev.duckdns.org", port=1883)    
    client.loop_start()
    while True:
        json_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "host": "server01"
                },
                "fields": {
                    "value": read_temperature(),
                }
            }
        ]
        client.publish("sensors/thermometer/1", json.dumps(json_body))
        print(f"published data {json_body}!")
        time.sleep(random.randint(2,5))
    print("loop break")
    client.disconnect()
    client.loop_stop()


