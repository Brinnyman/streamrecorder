import getopt
import sys
from streamrecorder import StreamRecorder


def main(argv):
    """Exectute command line options."""
    sr = StreamRecorder()

    usage = 'Usage: streamrecorder [options]\n'
    usage += '\n'
    usage += 'Options:\n'
    usage += '-h, --help        prints this message\n'
    usage += '-n, --name        streamer channel\n'
    usage += '-u, --url         stream url\n'
    usage += '-q, --quality     recording quality, first that is available <720p, 720p60, 1080p, 1080p60, best>. You can override these by providing the quality or pick the default Streamlink settings <best> or <worst>.\n'
    usage += '-r, --recordpath  recording path\n'
    usage += '-c, --commands    additional streamlink commands\n'
    usage += '-t, --type        recording type <twitch, vod, stream, record, play>\n'
    usage += '-v, --vod         twitch vod id\n'
    usage += '-i, --info        twitch stream information\n'

    if len(sys.argv) <= 1:
        print(usage)
        sys.exit(1)

    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'hn:u:q:r:c:t:v:i', ['name=', 'url=', 'quality=', 'recordpath=', 'commands=', 'type=', 'vod=', 'info'])
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)

    for option, arg in options:
        if option == '-h':
            print(usage)
            sys.exit()
        elif option in ('-n', '--name'):
            sr.name = arg
        elif option in ('-u', '--url'):
            sr.url = arg
        elif option in ('-q', '--quality'):
            sr.quality = arg
        elif option in ('-r', '--recordpath'):
            sr.recording_path = arg
        elif option in ('-c', '--commands'):
            sr.streamlink_commands = arg
        elif option in ('-t', '--type'):
            sr.type = arg
        elif option in ('-v', '--vod'):
            sr.vod_id = arg
        elif option in ('-i', '--info'):
            sr.twitch_stream_info()

    sr.run()


if __name__ == "__main__":
    main(sys.argv[1:])
