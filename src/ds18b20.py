# coding: utf8
import re
import traceback
from argparse import ArgumentParser

from w1 import W1Reader


class TemperatureReaderException(Exception):
    pass


class DS18B20TemperatureReader:
    """
    DS18B20 temperature sensor reader
    """

    _STATUS_PATTERN = re.compile(r"^[a-z0-9 ]+ : crc=[a-z0-9]+ (.+)$")
    _VALUE_PATTERN = re.compile(r"^[a-z0-9 ]+ t=([0-9]+)$")
    _STATUS_OK = "YES"

    def __init__(self, device_id):
        self._device_id = device_id
        try:
            self._w1_reader = W1Reader(self._device_id)
        except IOError as e:
            raise TemperatureReaderException(
                f"DS18B20 temperature sensor with id {self._device_id} not found: {e}") from e

    def read_temperature_celsius(self) -> float:
        data = self._w1_reader.read_data()
        celsius = self._parse_data(data)
        return celsius

    @staticmethod
    def _parse_data(data: str) -> float:
        if data is None:
            raise TemperatureReaderException("No data")

        lines = data.split("\n")
        match = DS18B20TemperatureReader._STATUS_PATTERN.match(lines[0])
        if match:
            status = match.group(1)
            if status != DS18B20TemperatureReader._STATUS_OK:
                raise TemperatureReaderException("Error status read from data: '{}'".format(status))
            elif len(lines) > 1:
                match = DS18B20TemperatureReader._VALUE_PATTERN.match(lines[1])
                if match:
                    celsius_str = match.group(1)
                    try:
                        return float(celsius_str) / 1000.0
                    except ValueError:
                        raise TemperatureReaderException("Cannot parse temperature info: '{}'".format(celsius_str))
                else:
                    raise TemperatureReaderException("Cannot parse second (value) data line: '{}'".format(lines[1]))
            else:
                raise TemperatureReaderException("Missing value line in data")
        else:
            raise TemperatureReaderException("Cannot parse first (status) data line: '{}'".format(lines[0]))


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--device-id", help="device id", default=None)
    arg_parser.add_argument("--count", help="number of read", type=int, default=1)
    arg_parser.add_argument("--sleep", help="number of seconds between 2 readings", type=int, default=1)
    args = arg_parser.parse_args()
    if args.device_id is None:
        print(f"Please provide a --device-id arg.")
        print(f"Detected device ids: {', '.join(W1Reader.get_device_ids())}")
    reader = DS18B20TemperatureReader(args.device_id)
    for i in range(args.count):
        try:
            print(reader.read_temperature_celsius())
        except:
            traceback.print_exc()


def _test():
    data = (
        "4c 01 55 05 7f a5 a5 66 04 : crc=04 YES\n"
        "4c 01 55 05 7f a5 a5 66 04 t=20750"
    )
    print(DS18B20TemperatureReader._parse_data(data))


if __name__ == '__main__':
    #_test()
    main()
