from enum import Enum


class SensorType(Enum):
    VISION = 1
    AUDIO = 2
    TEXT = 3
    NUMBER = 4
    MIX = 5


class Sensor:
    def __init__(self, sensor_name=None, sensor_type=None, sensor_agent=None, device=None):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.sensor_agent = sensor_agent
        self.device = device

    def
