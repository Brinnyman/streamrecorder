import os
import configparser


class StreamRecorder:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
        self.name = config['SETUP']['NAME']
        self.url = config['SETUP']['URL']
        self.recording_path = config['SETUP']['RECORDING_PATH']
        self.streamlink_path = config['STREAMLINK']['STREAMLINK_PATH']
        self.streamlink_quality = config['STREAMLINK']['STREAMLINK_QUALITY']
        self.streamlink_commands = config['STREAMLINK']['STREAMLINK_COMMANDS']
        self.ffmpeg_path = config['FFMPEG']['FFMPEG_PATH']
        self.twitch_client_id = config['TWITCH']['TWITCH_CLIENT_ID']
        self.vod_id = '380587447'

    def run(self):
        print('Starting streamrecorder')
