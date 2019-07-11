import os
import configparser
import time
from twitch.api import TwitchAPI
from recorder.recorder import Recorder
from player.player import Player
from helpers.filesystem import Filesystem
from helpers.contactsheet import ContactSheet


twitch_api = TwitchAPI()
r = Recorder()
p = Player()
f = Filesystem()
cs = ContactSheet()


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
        self.contact_sheet_extension = config['VCSI']['CONTACT_SHEET_EXTENSION']

    def twitch_stream_info(self):
        print(twitch_api.get_stream_information(self.name, self.twitch_client_id))

    def run(self):
        title = " ____  _                            ____                        _           \n"
        title += "/ ___|| |_ _ __ ___  __ _ _ __ ___ |  _ \ ___  ___ ___  _ __ __| | ___ _ __ \n"
        title += "\___ \| __| '__/ _ \/ _` | '_ ` _ \| |_) / _ \/ __/ _ \| '__/ _` |/ _ \ '__|\n"
        title += " ___) | |_| | |  __/ (_| | | | | | |  _ <  __/ (_| (_) | | | (_| |  __/ |\n"   
        title += "|____/ \__|_|  \___|\__,_|_| |_| |_|_| \_\___|\___\___/|_|  \__,_|\___|_|\n"
        title += '\n'
        start = 'Starting streamrecorder'
        print(title)
        
        if self.type == 'twitch':
            print(start)
            while True:
                status = twitch_api.get_stream_status(self.name, self.twitch_client_id)
                if status == 1:
                    print(self.name, "online.")
                    self.url = 'twitch.tv/' + self.name
                    r.record(self.streamlink_path, self.url, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name, self.streamlink_commands)
                time.sleep(15)
        elif self.type == 'vod':
            print(start)
            r.record_twitch_vod(self.streamlink_path, self.vod_id, self.twitch_client_id, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name)
        elif self.type == 'stream':
            print(start)
            while True:
                r.record(self.streamlink_path, self.url, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name, self.streamlink_commands)
                time.sleep(15)
        elif self.type == 'record':
            print(start)
            r.record(self.streamlink_path, self.url, self.streamlink_quality, self.ffmpeg_path, self.recording_path, self.name, self.streamlink_commands)
        elif self.type == 'play':
            print(start)
            while True:
                p.play(self.streamlink_path, self.url, self.streamlink_quality)
                time.sleep(15)
        elif self.type == 'contact':
            print(start)
            cs.bulk_contact_sheet(f.filtered_files(self.recording_path, self.contact_sheet_extension))

        else:
            print(start)
            p.play(self.streamlink_path, self.url, self.streamlink_quality)