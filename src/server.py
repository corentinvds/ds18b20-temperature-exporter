# coding=utf-8
import time
from argparse import ArgumentParser

from prometheus_client import start_http_server

from metrics import add_temperature_metric, REGISTRY

if __name__ == '__main__':

    arg_parser = ArgumentParser()
    arg_parser.add_argument("--device-id", help="device id", required=True)
    arg_parser.add_argument("--room", help="room name", required=True)
    arg_parser.add_argument("--port", help="http port", type=int, default=80)
    args = arg_parser.parse_args()

    print(f"Starting with args {args} ...")

    add_temperature_metric(args.device_id, args.room)

    start_http_server(args.port, registry=REGISTRY)

    print(f"Server started on port {args.port}")
    while True:
        time.sleep(.5)
