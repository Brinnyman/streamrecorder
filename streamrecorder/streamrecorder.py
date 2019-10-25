import asyncio
from plugin.twitch import TwitchStream
from plugin.cb import CbStream
from helpers.recorder import Recorder
from helpers.filesystem import Filesystem


class Streamrecorder:
    def __init__(self, url, quality, recording_path, stream_type, enable_contactsheet, ffmpeg_path, vcsi_path):
        self.url = url
        self.stream_type = stream_type
        self.quality = quality
        self.recording_path = recording_path
        self.enable_contactsheet = enable_contactsheet
        self.ffmpeg_path = ffmpeg_path
        self.vcsi_path = vcsi_path

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
            channel = TwitchStream(self.url)
            channel.quality = self.quality
            if channel._get_streams():
                if channel.stream_type == "live":
                    while True:
                        print("{} is live".format(channel.channel))
                        f = Filesystem()
                        f.create_directory(self.recording_path, channel.channel)
                        name = channel.channel  + '_' + channel.recorded_at
                        filename = f.create_file(name, 'mkv')
                    
                        recording = {
                            "uri": channel._get_streams(),
                            "output": filename,
                            "enable_contactsheet": self.enable_contactsheet
                        }

                        recorder = Recorder(self.ffmpeg_path, self.vcsi_path, recording)
                        await asyncio.gather(recorder.record())
                        await asyncio.sleep(15)
                elif channel.stream_type == "video":
                    print("{} is available".format(channel.channel))
                    f = Filesystem()
                    f.create_directory(self.recording_path, channel.channel)
                    name = channel.channel  + '_' + channel.recorded_at
                    filename = f.create_file(name, 'mkv')
                   
                    recording = {
                        "uri": channel._get_streams(),
                        "output": filename,
                        "enable_contactsheet": self.enable_contactsheet
                    }
                    recorder = Recorder(self.ffmpeg_path, self.vcsi_path, recording)
                    await asyncio.gather(recorder.record())
            else:
                print(
                    "{} is offline or hosting another channel".format(channel.channel)
                )
                await asyncio.sleep(15)

        elif self.stream_type == "cb":
            channel = CbStream(self.url)
            channel.quality = self.quality
            if channel._get_streams():
                while True:
                    print("{} is live".format(channel.channel))
                    f = Filesystem()
                    f.create_directory(self.recording_path, channel.channel)
                    name = channel.channel  + '_' + channel.recorded_at
                    filename = f.create_file(name, 'mkv')
                   
                    recording = {
                        "uri": channel._get_streams(),
                        "output": filename,
                        "enable_contactsheet": self.enable_contactsheet
                    }

                    recorder = Recorder(self.ffmpeg_path, self.vcsi_path, recording)
                    await asyncio.gather(recorder.record())
            else:
                print(
                    "{} is offline or hosting another channel".format(
                        channel.channel
                    )
                )
                await asyncio.sleep(15)

# TODO returning an object from _get_streams with type, uri, name, date also removes the need to separate the twitch live and video streams
