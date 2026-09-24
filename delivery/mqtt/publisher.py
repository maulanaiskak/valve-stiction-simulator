"""MQTT delivery adapter: publishes domain.Simulator's output as JSON
samples. No signal-generation logic here -- that's domain's job.
"""

from __future__ import annotations

import json
import time

import paho.mqtt.client as mqtt

from domain.simulator import Simulator


def run(
    broker_host: str,
    broker_port: int,
    topic: str,
    sensor_id: str,
    sim: Simulator,
    sample_interval_s: float,
) -> None:
    client = mqtt.Client(client_id=f"simulator-{sensor_id}")
    client.connect(broker_host, broker_port)
    client.loop_start()

    print(
        f"Simulator started: sensor_id={sensor_id} stiction={sim.stiction_enabled} "
        f"-> {broker_host}:{broker_port}/{topic}"
    )

    while True:
        pv, op = sim.step()
        payload = {
            "sensor_id": sensor_id,
            "pv": pv,
            "op": op,
            "ts": int(time.time() * 1000),
        }
        client.publish(topic, json.dumps(payload))
        time.sleep(sample_interval_s)
