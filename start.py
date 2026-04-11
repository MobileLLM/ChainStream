# helper file of chainstream
# it parses command arguments and send the options to ChainStream
import yaml
import argparse
import logging
# import chainstream as cs
from chainstream.runtime import cs_server
logging.basicConfig(
    level=logging.DEBUG,  # 设置为DEBUG级别以显示所有日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # 强制重新配置日志，覆盖之前的配置
)


def parse_args():
    """
    parse command line input
    generate options including host name, port number
    """
    parser = argparse.ArgumentParser(description="Start ChainStream server.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", action="store", dest="output_dir", default="output",
                        help="directory of output")
    parser.add_argument("-verbose", action="store_true", dest="verbose", default=False,
                        help="run in verbose mode")
    parser.add_argument("--platform", action='store', dest='platform', default='web',
                        choices=['web', 'shell'], 
                        help='runtime core server platform: web or shell')
    parser.add_argument("--enable-java", action="store_true", dest="enable_java", default=False,
                        help="enable Java agent support")
    args = parser.parse_args()

    # with open("./config.yaml", 'r') as stream:
    #     yaml_config = yaml.safe_load(stream)
        # merge yaml config with command line options

    # print options
    return args


def main():
    args = parse_args()
    cs_server.init(args.platform)
    cs_server.config(
        output_dir=args.output_dir,
        verbose=True,
        # monitor_mode='web'
    )

    # 启动gRPC桥接服务器（如果启用Java支持或使用Web平台）
    if args.enable_java or args.platform == 'web':
        start_grpc_bridge_server()

    # config_chainstream_server(
    #     output_dir=args.output_dir,
    #     verbose=True,
    #     monitor_mode='shell'
    # )
    cs_server.start()


def start_grpc_bridge_server():
    """启动gRPC桥接服务器"""
    try:
        from chainstream.runtime.java.grpc_server import start_bridge_server
        # 获取Runtime Core实例
        runtime_core = cs_server.get_chainstream_core()
        server = start_bridge_server(port=50051, runtime_core=runtime_core)
        if server:
            logging.info("gRPC Bridge Server started successfully on port 50051")
        else:
            logging.error("Failed to start gRPC Bridge Server")
    except Exception as e:
        logging.error(f"Error starting gRPC Bridge Server: {e}")


if __name__ == "__main__":
    main()

