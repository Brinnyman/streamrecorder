import asyncio
from plugin.twitch import TwitchStream
from plugin.cb import CbStream
from recorder.recorder import Recorder


class Streamrecorder:
    def __init__(self, url, quality, recording_path, stream_type, enable_contactsheet):
        self.url = url
        self.stream_type = stream_type
        self.quality = quality
        self.recording_path = recording_path
        self.enable_contactsheet = enable_contactsheet

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
                        recorder = Recorder()
                        await asyncio.gather(
                            recorder.record(
                                self.recording_path, channel, self.enable_contactsheet
                            )
                        )
                        await asyncio.sleep(15)
                elif channel.stream_type == "video":
                    print("{} is available".format(channel.channel))
                    recorder = Recorder()
                    await asyncio.gather(
                        recorder.record(
                            self.recording_path, channel, self.enable_contactsheet
                        )
                    )
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
                    recorder = Recorder()
                    await asyncio.gather(
                        recorder.record(
                            self.recording_path, channel, self.enable_contactsheet
                        )
                    )
            else:
                print(
                    "{} is offline or hosting another channel".format(
                        channel.channel
                    )
                )
                await asyncio.sleep(15)

# TODO returning an object from _get_streams with type, uri, name, date also removes the need to separate the twitch live and video streams
