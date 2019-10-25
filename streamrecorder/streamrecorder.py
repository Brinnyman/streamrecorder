import asyncio
from plugin.twitch import TwitchStream
from plugin.cb import CbStream
from helpers.recorder import Recorder
from helpers.filesystem import Filesystem
from helpers.contactsheet import ContactSheet


class Streamrecorder:
    def __init__(self, url, quality, recording_path, stream_type, enable_contactsheet, ffmpeg_path, vcsi_path):
        self.url = url
        self.stream_type = stream_type
        self.quality = quality
        self.recording_path = recording_path
        self.enable_contactsheet = enable_contactsheet
        self.ffmpeg_path = ffmpeg_path
        self.vcsi_path = vcsi_path

    def prepare_stream(self, stream):
        f = Filesystem()
        uri = stream._get_streams()

        f.create_directory(self.recording_path, stream.channel)
        f.create_file((stream.channel  + '_' + stream.recorded_at), 'mkv')
        filepath = f.create_filepath(f.get_directory(), f.get_filename())

        stream = {
            'stream_type': stream.stream_type,
            'channel': stream.channel,
            'uri': uri,
            'filepath': filepath
        }
        return stream

    async def run(self):
        title = " ____  _                            ____                        _           \n"
        title += "/ ___|| |_ _ __ ___  __ _ _ __ ___ |  _ \ ___  ___ ___  _ __ __| | ___ _ __ \n"
        title += "\___ \| __| '__/ _ \/ _` | '_ ` _ \| |_) / _ \/ __/ _ \| '__/ _` |/ _ \ '__|\n"
        title += " ___) | |_| | |  __/ (_| | | | | | |  _ <  __/ (_| (_) | | | (_| |  __/ |\n"
        title += "|____/ \__|_|  \___|\__,_|_| |_| |_|_| \_\___|\___\___/|_|  \__,_|\___|_|\n"
        title += "\n"
        start = "Starting streamrecorder"
        print(title)
        print(start)

        if self.stream_type == "twitch":
            twitch = TwitchStream(self.url, self.quality)
            stream = self.prepare_stream(twitch)
            if stream['uri']:
                if stream['stream_type'] == 'live':
                    while True:
                        print("{} is available".format(stream['channel']))
                        recorder = Recorder(self.ffmpeg_path)
                        await asyncio.gather(recorder.record(stream['uri'], stream['filepath']))
                        if self.enable_contactsheet:
                            cs = ContactSheet(self.vcsi_path)
                            cs.create_contact_sheet(stream['filepath'])
                        await asyncio.sleep(15)
                elif stream['stream_type'] == 'video':
                    print("{} is available".format(stream['channel']))
                    recorder = Recorder(self.ffmpeg_path)
                    await asyncio.gather(recorder.record(stream['uri'], stream['filepath']))
                    if self.enable_contactsheet:
                        cs = ContactSheet(self.vcsi_path)
                        cs.create_contact_sheet(stream['filepath'])
            else:
                print("{} is offline or hosting another channel".format(stream['channel']))
                await asyncio.sleep(15)

        elif self.stream_type == "cb":
            cb = CbStream(self.url, self.quality)
            stream = self.prepare_stream(cb)
            if stream['uri']:
                while True:
                    print("{} is available".format(stream['channel']))
                    recorder = Recorder(self.ffmpeg_path)
                    await asyncio.gather(recorder.record(stream['uri'], stream['filepath']))
                    if self.enable_contactsheet:
                        cs = ContactSheet(self.vcsi_path)
                        cs.create_contact_sheet(stream['filepath'])
                    await asyncio.sleep(15)
            else:
                print("{} is offline".format(stream['channel']))
                await asyncio.sleep(15)
                