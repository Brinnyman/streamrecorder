import argparse
import configparser
import os
import sys
import asyncio
import selectors
from streamrecorder import Streamrecorder


def main(args):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), './config.ini'))
    stream_name = args.stream_name or ''
    stream_id = args.stream_id or ''
    recording_path = args.path or config['SETUP']['RECORDING_PATH']
    stream_type = args.stream_type or ''
    quality = args.stream_quality or ''
    enable_contactsheet = args.enable_contactsheet or None
    
    sr = Streamrecorder(stream_name, stream_id, stream_type, quality, recording_path, enable_contactsheet)

    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
    elif sys.platform == 'darwin':
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
    my_parser = argparse.ArgumentParser(prog='streamrecorder', description='Record a stream', allow_abbrev=False)
    my_parser.add_argument('-n', metavar='name', dest='stream_name', type=str,
                           help='stream name')
    my_parser.add_argument('-t', dest='stream_type', type=str, choices=['stream', 'vod', 'cb'],
                           help='stream type')
    my_parser.add_argument('-i', metavar='id', dest='stream_id', type=str, help='Twitch stream identification')
    my_parser.add_argument('-p', metavar='path', dest='path', type=str, help='recording path')
    my_parser.add_argument('-q', metavar='quality', dest='stream_quality', type=str, help='stream quality')
    my_parser.add_argument('-c', dest='enable_contactsheet', action='store_false',
                           help='disable contactsheet generation')
    args = my_parser.parse_args()
    main(args)
