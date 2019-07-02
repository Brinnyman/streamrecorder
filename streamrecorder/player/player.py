import subprocess
import sys
import time


class Player:
    def player(self, streamlink_path, url, quality, *args):
        try:
            print('start streamlink')
            streamlink = [streamlink_path, url, quality] + list(args)
            subprocess.call(streamlink)
            print('close streamlink')

        except OSError:
            print('An error has occurred while trying to use streamlink package. Is it installed? Do you have Python in your PATH variable?')
            sys.exit(1)
        except KeyboardInterrupt:
            print('Processes are being terminated')
            sys.exit(1)
        return

    def play(self, streamlink_path, url, streamlink_quality):
        self.player(streamlink_path, url, streamlink_quality)