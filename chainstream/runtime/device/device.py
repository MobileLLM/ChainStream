from enum import Enum
import collections
import websocket


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

        self.sensor_list = collections.OrderedDict()
        self.agent_list = collections.OrderedDict()

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


class SocketDeviceBase(DeviceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws = websocket.WebSocketApp(
            self.device_meta.device_id,
        )

    def check_sensor_list(self):
        sensor_list = None

        def check_sensor(ws):
            ws.send("check_sensors")

        def on_message(ws, message):
            global sensor_list
            sensor_list = message

        ws = websocket.WebSocketApp(
            self.device_meta.device_id,
            on_open=check_sensor,
            on_message=on_message,
        )
