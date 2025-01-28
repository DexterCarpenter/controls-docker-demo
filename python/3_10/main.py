import paho.mqtt.client as mqtt
import logging
import threading
import json
import time

# Lorenz System Parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

# Initial conditions
x, y, z = 1.0, 1.0, 1.0
dt = 0.01  # Time step for numerical integration

# Define the callback for when a connection is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("cmd/#")  # Subscribe to a topic

# Define the callback for when a message is received
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    logging.warning(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

# Function to compute the next step in the Lorenz system
def update_lorenz():
    global x, y, z
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    x += dx
    y += dy
    z += dz
    return x, y, z

# Function to publish Lorenz system values as JSON messages
def publish_message():
    x, y, z = update_lorenz()  # Update system state

    # Create a JSON payload with Lorenz values
    payload = {
        "id": 1,
        "name": "lorenz_simulation",
        "status": "active",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": {
            "x": round(x, 4),
            "y": round(y, 4),
            "z": round(z, 4)
        }
    }
    
    # Convert the dictionary to a JSON string
    json_payload = json.dumps(payload)

    # Publish the JSON message to the MQTT topic
    client.publish("data/lorenz", json_payload)
    print(f"Message published: {json_payload}")

    # Schedule the function to run again after 0.5 seconds
    threading.Timer(0.5, publish_message).start()

# Create an MQTT client instance
client = mqtt.Client()

# Attach the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("mosquitto", 1883, 60)

# Start the repeating message publishing
publish_message()

# Blocking loop to process network traffic and callbacks
client.loop_forever()