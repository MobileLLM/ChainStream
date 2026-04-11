import websocket


def default_on_message(ws, message):
    print(f"收到服务器消息: {message}")


def default_on_error(ws, error):
    print(f"WebSocket错误发生: {error}")


def default_on_close(ws, close_status_code, close_msg):
    print("WebSocket连接已关闭")


class WebSocketClient:
    def __init__(self, server_address, on_start_message=None, on_error=default_on_error,
                 on_close=default_on_close, on_message=default_on_message):
        self.on_start_message = on_start_message
        self.server_address = server_address
        self.ws = websocket.WebSocketApp(server_address,
                                         on_open=self.on_open,
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close)

    def on_open(self, ws):
        print("WebSocket连接已打开")
        if self.on_start_message:
            self.send_message(self.on_start_message)

    def start(self):
        print(f"连接到服务器: {self.server_address}")
        self.ws.run_forever()

    def send_message(self, message):
        self.ws.send(message)

    def close(self):
        self.ws.close()


if __name__ == "__main__":
    # 替换成你的服务器地址
    server_address = "ws://172.20.10.8:6666"

    # 创建WebSocket客户端实例
    client = WebSocketClient(server_address, on_start_message="video,1,0")

    try:
        # 启动WebSocket连接
        client.start()


    finally:
        # 关闭WebSocket连接
        client.close()
