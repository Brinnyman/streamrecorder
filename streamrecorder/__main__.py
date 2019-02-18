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
    usage += '-i, --info        twitch stream information\n'

    if len(sys.argv) <= 1:
        print(usage)
        sys.exit(1)

    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'hin:', ['info=', 'name='])
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
        elif option in ('-i', '--info'):
            sr.twitch_stream_info()

    sr.run()


if __name__ == "__main__":
    main(sys.argv[1:])
