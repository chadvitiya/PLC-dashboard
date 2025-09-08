import snap7
from azure.iot.device import IoTHubDeviceClient, Message
import json
import time

# Connect to PLC
plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)

# Azure IoT Device connection string
conn_str = "HostName=arcreate.azure-devices.net;DeviceId=(owndevicestring)"
client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# Memory map for XRcreate signals
bit_mapping = {
    "case1": (0, 0),
    "case2": (0, 1),
    "case3": (0, 2),
    "case4": (0, 3),
    "case5": (0, 4),
    "case6": (0, 5),
    "case7": (0, 6),
    "case8": (1, 0),
    "case9": (1, 1),
    "case10": (1, 2),
    "case11": (1, 3),
    "case12": (1, 4),
    "case13": (1, 5),
    "case14": (1, 6),
    "case15": (2, 0),
    "pump1": (3, 0),
    "pump2": (3, 1)
}

def handle_c2d_message(message):
    print("Received C2D message:", message.data)

    try:
        # XRcreate sends double-encoded string
        step1 = json.loads(message.data)
        step2 = json.loads(step1)

        formatted = {
            "deviceId": "f2124164-ab35-4412-aeb6-970c0c1fed9b"
        }

        for key, (byte_index, bit_index) in bit_mapping.items():
            if key in step2:
                val = step2[key]
                if isinstance(val, str) and val.lower() in ["true", "false"]:
                    val = val.lower() == "true"
                elif isinstance(val, bool):
                    val = val
                else:
                    continue  # Ignore invalid values

                # Write to PLC memory bit
                data = plc.mb_read(byte_index, 1)
                snap7.util.set_bool(data, 0, bit_index, val)
                plc.mb_write(byte_index,1, data)

                formatted[key] = val

        # Echo back to XRcreate
        echo_msg = Message(json.dumps(formatted))
        client.send_message(echo_msg)
        print(f"Written to PLC and echoed back: {formatted}")

    except Exception as e:
        print(f"Error processing message: {e}")

client.on_message_received = handle_c2d_message

print("Listening for messages from XRcreate and writing to PLC...")
while True:
    time.sleep(1)