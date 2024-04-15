from typing import List, Dict, Any
from interfaces import Interfaces
from dotenv import dotenv_values
from machine_sub_handler import machine_handler
import paho.mqtt.client as mqtt
import logging
import threading
import uuid


class Device:
    """
    Represents a device that connects to an MQTT broker.
    """

    def __init__(self) -> None:
        """
        Initializes the Device object and connects to the MQTT broker.
        """
        self.interfaces = Interfaces(protocol='mqtt')
        self.__device_interfaces: List[Dict[str, Any]] = self.get_device_interfaces()
        self.__device_id: Any = self._device_id()
        self.__device_mac: Any = NotImplemented

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.username_pw_set(config.get('MQTT_USERNAME'), config.get('MQTT_PASSWORD'))

        self.mqttc.connect(config.get('MQTT_HOST'), int(config.get('MQTT_PORT')), int(config.get('KEEPALIVE')))

        threading.Thread(target=self.mqttc.loop_forever).start()

    def get_device_interfaces(self) -> List[Dict[str, Any]]:
        """
        Filters a list of interface dictionaries, returning only those with 'ownership' set to 'device'.

        Returns:
        - List[Dict[str, Any]], the filtered list of interface dictionaries.
        """
        _interfaces: List[Dict[str, Any]] = self.interfaces.get_interfaces()

        return list(filter(lambda interface: interface['ownership'] == 'device', _interfaces))

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict[str, Any], reason_code: int,
                   properties: Any) -> None:
        """
        Callback function called when the client successfully connects to the MQTT broker.

        Parameters:
        - client: mqtt.Client, the MQTT client object.
        - userdata: Any, user-defined data.
        - flags: Dict[str, Any], connection flags.
        - reason_code: int, the connection result code.
        - properties: Any, connection properties.
        """
        logger.debug(f"Connected with result code {reason_code}")
        # create an array tuple of device interfaces and qos using lambda
        _ = list(
            map(lambda interface: (interface['interface_name'].replace('<device_id>', self.__device_id), 1),
                self.interfaces.get_interfaces()))
        client.subscribe(_)  # subscribe to the interfaces

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        """
        Callback function called when a message is received from the MQTT broker.

        Parameters:
        - client: mqtt.Client, the MQTT client object.
        - userdata: Any, user-defined data.
        - msg: mqtt.MQTTMessage, the received message.
        """
        machine_handler(client, userdata, msg)

    def publish(self, topic: str, payload: Any) -> None:
        """
        Publishes a message to the MQTT broker.

        Parameters:
        - topic: str, the topic to publish to.
        - payload: str, the message payload.
        """
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.username_pw_set(config.get('MQTT_USERNAME'), config.get('MQTT_PASSWORD'))
        self.mqttc.connect(config.get('MQTT_HOST'), int(config.get('MQTT_PORT')), int(config.get('KEEPALIVE')))

        logger.debug(f"Publishing message to topic {topic}")

        self.mqttc.publish(topic, payload=payload)

    def _device_id(self) -> Any:
        """
        Gets the device ID.

        Returns:
        - Any, the device ID.
        """
        return hex(uuid.getnode()).strip('0x')


if __name__ == '__main__':
    config: Dict[str, str] = dotenv_values(".env")

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    device = Device()
