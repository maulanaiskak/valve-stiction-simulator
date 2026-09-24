"""Entrypoint: env vars -> domain.Simulator + delivery.mqtt.publisher.
All the actual logic lives in those two modules.
"""

from __future__ import annotations

import os

from delivery.mqtt.publisher import run
from domain.simulator import Simulator


def main() -> None:
    broker_host = os.environ.get("MQTT_BROKER_HOST", "localhost")
    broker_port = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
    topic = os.environ.get("MQTT_TOPIC", "valve/data")
    sensor_id = os.environ.get("SENSOR_ID", "valve-1")
    stiction_enabled = os.environ.get("STICTION_ENABLED", "false").lower() == "true"
    sample_interval_s = float(os.environ.get("SAMPLE_INTERVAL_S", "0.1"))

    sim = Simulator(stiction_enabled=stiction_enabled)
    run(broker_host, broker_port, topic, sensor_id, sim, sample_interval_s)


if __name__ == "__main__":
    main()
