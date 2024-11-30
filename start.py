# helper file of chainstream
# it parses command arguments and send the options to ChainStream
import yaml
import argparse
import logging
# import chainstream as cs
from chainstream.runtime import cs_server
logging.basicConfig(level=logging.INFO)


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

    # config_chainstream_server(
    #     output_dir=args.output_dir,
    #     verbose=True,
    #     monitor_mode='shell'
    # )
    cs_server.start()


if __name__ == "__main__":
    main()

