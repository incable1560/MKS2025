import paho.mqtt.client as mqtt
import json
import base64

PC_NUMBER = "71"   # ← sem doplň svoje číslo PC !!
TOPIC = f"v3/mpc-mks@ttn/devices/devkit-81/up"

BROKER = "eu1.cloud.thethings.network"
PORT = 1883
USERNAME = "mpc-mks@ttn"
PASSWORD = "NNSXS.B75L4YCIWKRIXUGEDS2NNGXTNAV4PHW7POSNS2Y.EE42KQNJKP36YCSLRH5SIU4I5XXC2KOQGJPIT3PRK4PKNMPDNIVQ"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to TTN MQTT broker!")
    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC}")


def on_message(client, userdata, msg):
    try:
        # Convert bytes → string
        payload_str = msg.payload.decode("utf-8")

        # Convert JSON string → dict
        pld = json.loads(payload_str)

        # Extract fields
        time = pld["received_at"]
        frequency = pld["uplink_message"]["settings"]["frequency"]
        frm_payload = pld["uplink_message"]["frm_payload"]

        # Base64 decode
        decoded_msg = base64.b64decode(frm_payload).decode()

        print("----------------------------------")
        print("Time:", time)
        print("Frequency:", frequency)
        print("Message:", decoded_msg)

    except Exception as e:
        print("Error parsing message:", e)
        print("Raw data:", msg.payload)


# Create client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Set username/password
mqttc.username_pw_set(USERNAME, PASSWORD)

# Connect to TTN
mqttc.connect(BROKER, PORT, 60)

# Start loop
mqttc.loop_forever()
