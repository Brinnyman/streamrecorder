import subprocess
import sys

class Recorder:
    def __init__(self):
        self.streamlink_path = 'streamlink'
        self.ffmpeg_path = 'ffmpeg'

    # TODO: make quality optional because of vod recordings?
    def record(self, url, recorded_file, quality, *args):
        process = None
        try:
            print('Recording in session.')
            
            print('start streamlink')
            streamlink = [self.streamlink_path, url, quality, '--stdout'] + list(args)
            process = subprocess.Popen(streamlink, stdout=subprocess.PIPE, stderr=None)

            print('start ffmpeg')
            ffmpeg = [self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', 'pipe:0', '-c', 'copy', recorded_file, '-loglevel', 'quiet']
            process2 = subprocess.Popen(ffmpeg, stdin=process.stdout, stdout=subprocess.PIPE, stderr=None)

            process.stdout.close()
            process2.communicate()
            print('Recording is done.')

        except OSError:
            print('An error has occurred while trying to use livestreamer package. Is it installed? Do you have Python in your PATH variable?')
            sys.exit(1)

        return process2.stdout