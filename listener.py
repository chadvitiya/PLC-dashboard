# listener.py
import snap7
import json
import time
from azure.iot.device import IoTHubDeviceClient

# Connect to PLC
plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)

# Azure IoT connection
conn_str = "HostName=advitiya-iothub.azure-devices.net;DeviceId=PLC;SharedAccessKey=(owndevicestring)"
client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# Correct case bit mapping
CASE_BIT_MAPPING = {
    "case1":  (0, 0),
    "case2":  (0, 1),
    "case3":  (0, 2),
    "case4":  (0, 3),
    "case5":  (0, 4),
    "case6":  (0, 5),
    "case7":  (0, 6),
    "case8":  (1, 0),
    "case9":  (1, 1),
    "case10": (1, 2),
    "case11": (1, 3),
    "case12": (1, 4),
    "case13": (1, 5),
    "case14": (1, 6),
    "case15": (2, 0),
    "pump1":  (3, 0),
    "pump2":  (3, 1)
}

def message_handler(message):
    try:
        data = json.loads(message.data)
        for key, value in data.items():
            if key not in CASE_BIT_MAPPING:
                continue

            byte_index, bit_index = CASE_BIT_MAPPING[key]
            plc_data = bytearray(1)
            snap7.util.set_bool(plc_data, 0, bit_index, value)
            plc.mb_write(byte_index, 1, plc_data)
            print(f"{key} set to: {'ON' if value else 'OFF'}")

    except Exception as e:
        print(f"Error: {e}")

client.connect()
client.on_message_received = message_handler
print("Listening for cloud messages...")

while True:
    time.sleep(1)

