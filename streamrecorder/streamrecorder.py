import time
import os
import configparser
import datetime
from helpers.filesystem import Filesystem
from twitch.api import TwitchAPI
from recorder.recorder import Recorder


twitch_api = TwitchAPI()
filesystem = Filesystem()
r = Recorder()


class StreamRecorder:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
        self.name = config['SETUP']['NAME']
        self.url = config['SETUP']['URL']
        self.recording_path = config['SETUP']['RECORDING_PATH']
        self.type = ''
        self.streamlink_path = config['STREAMLINK']['STREAMLINK_PATH']
        self.streamlink_quality = config['STREAMLINK']['STREAMLINK_QUALITY']
        self.streamlink_commands = config['STREAMLINK']['STREAMLINK_COMMANDS']
        self.ffmpeg_path = config['FFMPEG']['FFMPEG_PATH']
        self.twitch_client_id = config['TWITCH']['TWITCH_CLIENT_ID']
        self.vod_id = ''

    def record_twitch(self, recording_path, name, twitch_client_id, streamlink_quality, streamlink_commands):
        filesystem.create_directory(recording_path, name)
        print('Setup recorder')
        while True:
            status = twitch_api.get_stream_status(name, twitch_client_id)
            if status == 1:
                print(name, "online.")
                recorded_file = filesystem.create_file(name, datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
                url = 'twitch.tv/' + name
                r.record(url, recorded_file, streamlink_quality, streamlink_commands)
            
            time.sleep(15)
        return

    def record_twitch_vod(self, recording_path, name, twitch_client_id, vod_id, streamlink_quality):  
        info = twitch_api.get_vod_information(vod_id, twitch_client_id)
        filesystem.create_directory(recording_path, name)
        recorded_file = filesystem.create_file(info['channel']['name'], info['published_at'])
        url = 'twitch.tv/videos/' + vod_id
        r.record(url, recorded_file, streamlink_quality)

    def record_stream(self, url, recording_path, name, streamlink_quality):
        while True:
            filesystem.create_directory(recording_path, name)
            recorded_file = filesystem.create_file(name, datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
            r.record(url, recorded_file, streamlink_quality)
            time.sleep(15)

    def twitch_stream_info(self):
        print(twitch_api.get_stream_information(self.name, self.twitch_client_id))

    def run(self):
        start = 'Starting streamrecorder'
        if self.type == 'twitch':
            print(start)        
            self.record_twitch(self.recording_path, self.name, self.twitch_client_id, self.streamlink_quality, self.streamlink_commands)
        elif self.type == 'vod':
            print(start)        
            self.record_twitch_vod(self.recording_path, self.name, self.twitch_client_id, self.vod_id, self.streamlink_quality)
        elif self.type == 'stream':
            print(start)        
            self.record_stream(self.url, self.recording_path, self.name, self.streamlink_quality)
