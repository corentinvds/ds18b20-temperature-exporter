# coding=utf-8
import os
from typing import List


class W1Reader:
    """
    1-wire data reader
    """

    _W1_DEVICES_FOLDER = r"/sys/devices/w1_bus_master1"
    _W1_DATA_FILENAME = "w1_slave"

    def __init__(self, device_id):
        self._device_id = device_id
        self._data_file = os.path.join(W1Reader._W1_DEVICES_FOLDER, device_id, W1Reader._W1_DATA_FILENAME)
        if not os.path.exists(self._data_file):
            raise IOError(f"File '{self._data_file}' does not exist for device id {device_id}")

    def read_data(self) -> str:
        with open(self._data_file) as data_file:
            return data_file.read()

    @staticmethod
    def get_device_ids() -> List[str]:
        return [
            d for d in os.listdir(W1Reader._W1_DEVICES_FOLDER)
            if os.path.exists(os.path.join(W1Reader._W1_DEVICES_FOLDER, d, W1Reader._W1_DATA_FILENAME))
        ]
