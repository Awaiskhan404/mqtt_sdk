import json

import paho.mqtt.client as mqtt
from dotenv import dotenv_values
from typing import Any, Dict
import logging, os


def publish_to_cloud(interface: str, payload: Any) -> None:
    """
    Publishes a message to a specific cloud server.

    Parameters:
    - interface: str, the interface ID to publish to.
    - payload: Any, the message payload.
    """
    logger = logging.getLogger(__name__)

    #read .env and get the values
    config: Dict[str, str] = dotenv_values(".env")

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(config.get('MQTT_USERNAME','hw_node'), config.get('MQTT_PASSWORD', '3E2Q[#2Z[5fE'))
    mqttc.connect(config.get('MQTT_HOST', '20.221.112.128'), int(config.get('MQTT_PORT', '1883')), int(config.get('KEEPALIVE', '65000')))
    mqttc.publish(interface, payload=json.dumps(payload))

    mqttc.disconnect()

    logger.debug(f"Published event to cloud interface {interface}")

    return None
