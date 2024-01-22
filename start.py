# helper file of chainstream
# it parses command arguments and send the options to ChainStream
import argparse
import chainstream as cs


def parse_args():
    """
    parse command line input
    generate options including host name, port number
    """
    parser = argparse.ArgumentParser(description="Start ChainStream server.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", action="store", dest="output_dir",
                        help="directory of output")
    parser.add_argument("-verbose", action="store_true", dest="verbose", default=False,
                        help="run in verbose mode")
    args = parser.parse_args()
    # print options
    return args


def main():
    args = parse_args()
    cs_server = cs.runtime.ChainStreamServer(
        output_dir=args.output_dir,
        verbose=args.verbose
    )
    cs_server.start()


if __name__ == "__main__":
    main()