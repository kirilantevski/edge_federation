import json
import paho.mqtt.client as mqtt
import math

def compute_distance(x,y):
    distance = (x-coordinates["x"])*(x-coordinates["x"]) + (y-coordinates["y"])*(y-coordinates["y"])
    return distance

MQTT_IP="192.168.122.3"
MQTT_PORT=1883
MQTT_TOPIC="/experiment/location"

mqtt_federation_trigger = False
mqtt_federation_usage = False

coordinates = {"x": 30.4075826699, "y": -7.67201633367}
ap_x = float(30.4075826699)
ap_y = float(-7.67201633367)


def compute_distance(x,y):
    distance = float((x-ap_x)*(x-ap_x) + (y-ap_y)*(y-ap_y))
    print(distance)
    return math.sqrt(distance)

def on_connect(client, userdata, flags, rc):

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(msg)
    

    # Check for byte encoding just in case
    if type(msg.payload) == bytes:
        message = json.loads(msg.payload.decode("UTF-8"))
    else:
        message = json.loads(msg.payload)
    print(message)
    print("x:",float(message["center"][0]),"y",float(message["center"][1]))
    x = float(message["center"][0])
    y = float(message["center"][1])
    distance = compute_distance(x, y)
    print("Distance: ",distance)

    # print(message['center'])
    # if len(message["center"]):
    #     distance = compute_distance(float(message["center"][0]), float(message["center"][1]))

    if distance < 2.0:
        print("IN: Distance lower than 2")
    else:
        print("OUT")

    #MQTT_MSG=json.dumps({"center": [x1,y1],"radius":  3});
    #Customer ap coordinates: x: 30.4075826699 y: -7.67201633367
    # if distance < 2.0:
    #     mqtt_federation_trigger = True
    # else:
    #     mqtt_federation_trigger = False
if __name__ == '__main__':
    client = mqtt.Client(None, clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_IP, MQTT_PORT, 60)
    client.loop_forever()