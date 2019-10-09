import argparse
import sys
import asyncio
import selectors
from streamrecorder import Streamrecorder


def main(args):
    sr = Streamrecorder()
    sr.stream_name = args.stream_name
    sr.stream_id = args.stream_id
    sr.recording_path = args.path
    sr.stream_type = args.stream_type
    sr.quality = args.stream_quality
    sr.enable_contactsheet = args.enable_contactsheet

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
    my_parser.add_argument('-n', '--name', metavar='name', dest='stream_name', type=str, required=True,
                           help='stream name')
    my_parser.add_argument('-t', '--type', metavar='type', dest='stream_type', type=str, required=True,
                           help='stream type')
    my_parser.add_argument('-i', '--id', metavar='id', dest='stream_id', type=str, help='Twitch stream identification')
    my_parser.add_argument('-p', '--path', metavar='path', dest='path', type=str, help='recording path')
    my_parser.add_argument('-q', '--quality', metavar='quality', dest='stream_quality', type=str, help='stream quality')
    my_parser.add_argument('-c', '--contact', dest='enable_contactsheet', action='store_false',
                           help='disable contactsheet generation')
    args = my_parser.parse_args()
    main(args)
