from base_socket_action import BaseSocketActions


class AndroidLogAction(BaseSocketActions):
    def __init__(self, ip='192.168.43.1', port=6666):
        super().__init__(agent_id='android_log_action', cmd='log', stream_name='log_to_android')
