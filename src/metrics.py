# coding=utf-8
import time
from typing import List

from prometheus_client import Gauge, CollectorRegistry, start_http_server

# We do not want all the python metrics here. There are 2 ways to do that:
# 1) unregister metrics from the default prometheus_client.registry.REGISTRY:
# for coll in list(REGISTRY._collector_to_names.keys()):
#     REGISTRY.unregister(coll)
# 2) create a fresh registry with CollectorRegistry(auto_describe=False) and use it explicitly everywhere
from ds18b20 import DS18B20TemperatureReader

REGISTRY = CollectorRegistry(auto_describe=False)

TEMPERATURE = Gauge(
    name='temperature',
    documentation='Room Temperature',
    unit='celsius',
    labelnames=["room"],
    registry=REGISTRY)

TEMPERATURE_READ_DURATION = Gauge(
    name='temperatures_reading_duration',
    documentation='Time spent reading the temperatures',
    labelnames=["room"],
    unit="seconds",
    registry=REGISTRY)


def read_temperature(reader: DS18B20TemperatureReader, duration_gauge: Gauge):
    with duration_gauge.time():
        return reader.read_temperature_celsius()


def add_temperature_metric(device_id, room):
    reader = DS18B20TemperatureReader(device_id)
    TEMPERATURE.labels(room=room).set_function(
        lambda: read_temperature(reader, TEMPERATURE_READ_DURATION.labels(room=room)))
