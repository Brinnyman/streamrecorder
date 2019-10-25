import argparse
import configparser
import os
import sys
import asyncio
import selectors
from streamrecorder import Streamrecorder


def main(args):
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "./config.ini")
    )
    recording_path = args.path or config["SETUP"]["RECORDING_PATH"]
    url = args.url or ""
    quality = args.quality or ""
    stream_type = args.stream_type or ""
    enable_contactsheet = args.enable_contactsheet or None
    ffmpeg_path = config["FFMPEG"]["FFMPEG_PATH"]
    vcsi_path = config['VCSI']['VCSI_PATH']
    sr = Streamrecorder(url, quality, recording_path, stream_type, enable_contactsheet, ffmpeg_path, vcsi_path)

    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
    elif sys.platform == "darwin":
        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)
    else:
        loop = asyncio.get_event_loop()

    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(sr.run())
    finally:
        loop.close()


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(
        prog="streamrecorder", description="Record a stream", allow_abbrev=False
    )
    my_parser.add_argument("-u", metavar="url", dest="url", type=str, help="url")
    my_parser.add_argument(
        "-q", metavar="quality", dest="quality", type=str, help="quality"
    )
    my_parser.add_argument("-p", metavar="path", dest="path", type=str, help="path")
    my_parser.add_argument(
        "-t", metavar="stream_type", dest="stream_type", type=str, help="stream type"
    )
    my_parser.add_argument(
        "-c",
        dest="enable_contactsheet",
        action="store_false",
        help="disable contactsheet",
    )
    args = my_parser.parse_args()
    main(args)
