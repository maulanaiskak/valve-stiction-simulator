# valve-stiction-simulator

Synthetic valve simulator for the valve stiction fault-detection pipeline. Generates a triangle-wave OP (output/manipulated variable) and a stick-slip valve model's resulting PV (process variable), and publishes `{sensor_id, pv, op, ts}` JSON samples over MQTT. Consumed by [valve-stiction-ingestion](https://github.com/maulanaiskak/valve-stiction-ingestion).

Not closed-loop PI control — that was tried and could self-oscillate from integral windup against OP saturation even with a healthy valve. This directly scripts the OP and the valve's stick-slip response instead, same physics as [valve-stiction-ml](https://github.com/maulanaiskak/valve-stiction-ml)'s test fixtures, and its stiction toggle is verified against the real classic detector in `test_main.py`.

## Run

```bash
pip install paho-mqtt numpy
MQTT_BROKER_HOST=localhost SENSOR_ID=valve-1 STICTION_ENABLED=true python main.py
```

| Env var | Default |
|---|---|
| `MQTT_BROKER_HOST` | `localhost` |
| `MQTT_BROKER_PORT` | `1883` |
| `MQTT_TOPIC` | `valve/data` |
| `SENSOR_ID` | `valve-1` |
| `STICTION_ENABLED` | `false` |
| `SAMPLE_INTERVAL_S`, `PERIOD_SAMPLES`, `AMPLITUDE`, `STICK_BAND`, `NOISE_STD`, `CENTER` | signal-shape tuning, see `main.py` |
