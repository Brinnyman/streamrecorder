import os
import configparser
import time
from twitch.api import TwitchAPI
from recorder.recorder import Recorder
from player.player import Player


twitch_api = TwitchAPI()
r = Recorder()
p = Player()


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

    def twitch_stream_info(self):
        print(twitch_api.get_stream_information(self.name, self.twitch_client_id))

    def run(self):
        start = 'Starting streamrecorder'
        if self.type == 'twitch':
            print(start)        
            r.record_twitch(self.streamlink_path, self.twitch_client_id, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name, self.streamlink_commands)
        elif self.type == 'vod':
            print(start)        
            r.record_twitch_vod(self.streamlink_path, self.vod_id, self.twitch_client_id, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name)
        elif self.type == 'stream':
            print(start)        
            while True:
                r.record(self.streamlink_path, self.url, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name)
                time.sleep(15)
        elif self.type == 'record':
            print(start)
            r.record(self.streamlink_path, self.url, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name)
        elif self.type == 'play':
            print(start)
            while True:
                p.play(self.streamlink_path, self.url, self.streamlink_quality)
                time.sleep(15)
        else:
            print(start)
            p.play(self.streamlink_path, self.url, self.streamlink_quality)
