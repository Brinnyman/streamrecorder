import subprocess
import sys
import time
import datetime
from helpers.filesystem import Filesystem
from twitch.api import TwitchAPI

twitch_api = TwitchAPI()
filesystem = Filesystem()

class Recorder:
    # TODO: make quality optional because of vod recordings?
    # TODO: streamlink doesnt like empty arguments, so find a way to have them optional. e.g. streamlink_commands
    # TODO: make the functions more generic? 
    def recorder(self, streamlink_path, url, streamlink_quality, ffmpeg_path, recorded_file, *args):
        process = None
        try:
            print('Recording in session.')
            
            print('start streamlink')
            streamlink = [streamlink_path, url, streamlink_quality, '--stdout'] + list(args)
            process = subprocess.Popen(streamlink, stdout=subprocess.PIPE, stderr=None)

            print('start ffmpeg')
            ffmpeg = [ffmpeg_path, '-err_detect', 'ignore_err', '-i', 'pipe:0', '-c', 'copy', recorded_file, '-loglevel', 'quiet']
            process2 = subprocess.Popen(ffmpeg, stdin=process.stdout, stdout=subprocess.PIPE, stderr=None)

            process.stdout.close()
            process2.communicate()
            print('Recording is done.')

        except OSError:
            print('An error has occurred while trying to use livestreamer package. Is it installed? Do you have Python in your PATH variable?')
            sys.exit(1)
        except KeyboardInterrupt:
            print('Processes are being terminated')
            process.wait()
            process2.wait()
            sys.exit(1)

        return process2.stdout

    def record(self, streamlink_path, url, streamlink_quality, ffmpeg_path, recording_path, name, streamlink_commands):
        filesystem.create_directory(recording_path, name)
        recorded_file = filesystem.create_file(name, datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
        self.recorder(streamlink_path, url, streamlink_quality, ffmpeg_path,  recorded_file, streamlink_commands)

    def record_twitch(self, streamlink_path, twitch_client_id, streamlink_quality, ffmpeg_path, recording_path, name, streamlink_commands):
        filesystem.create_directory(recording_path, name)
        print('Setup recorder')
        while True:
            status = twitch_api.get_stream_status(name, twitch_client_id)
            if status == 1:
                print(name, "online.")
                recorded_file = filesystem.create_file(name, datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
                url = 'twitch.tv/' + name
                self.recorder(streamlink_path, url, streamlink_quality, ffmpeg_path,  recorded_file, streamlink_commands)
            
            time.sleep(15)

    def record_twitch_vod(self, streamlink_path, vod_id, twitch_client_id, streamlink_quality, ffmpeg_path, recording_path, name):  
        filesystem.create_directory(recording_path, name)
        info = twitch_api.get_vod_information(vod_id, twitch_client_id)
        recorded_file = filesystem.create_file(info['channel']['name'], info['published_at'])
        url = 'twitch.tv/videos/' + vod_id
        self.recorder(streamlink_path, url, streamlink_quality, ffmpeg_path, recorded_file)