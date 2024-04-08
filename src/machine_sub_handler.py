import paho.mqtt.client as mqtt
from typing import Any
from enums import MachineCommand


def machine_handler(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    """
    Callback function called when the client receives a message from the MQTT broker.

    Parameters:
    - client: mqtt.Client, the MQTT client object.
    - userdata: Any, user-defined data.
    - msg: mqtt.MQTTMessage, the message received.
    """
    print(f"Received event on interface '{msg.topic}'")

    if msg.topic == "mqtt.heisenberg.live.MachineEvent":
        if int(msg.payload.decode()) == MachineCommand.START.value:
            print("Switching on the machine")
        elif int(msg.payload.decode()) == MachineCommand.STOP.value:
            print("Switching off the machine")
        else:
            print("Invalid command")
