from enum import Enum


class DeviceOpType(Enum):
    ANDROID = 1
    LINUX = 2
    WINDOWS = 3


class DeviceConnectionType(Enum):
    LOCAL = 1
    LAN = 2
    PROXY = 3


class DeviceMeta:
    def __init__(self, *args, **kwargs):
        self.device_name = kwargs.get("device_name")
        self.device_id = kwargs.get("device_id")
        self.device_op_type = kwargs.get("device_op_type")
        self.device_connection_type = kwargs.get("device_connection_type")


class DeviceBase:
    def __init__(self, *args, **kwargs):
        self.device_meta = None
        self.refresh_device_meta(**kwargs)

    def refresh_device_meta(self, *args, **kwargs):
        # TODO: add refresh limit
        self.device_meta = DeviceMeta(**kwargs)

    def check_connectivity(self):
        raise NotImplementedError("check_connectivity method not implemented")

    def start_all(self):
        pass

    def start_sensor(self, sensor_name):
        pass

    def stop_all(self):
        pass




