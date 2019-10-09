import asyncio
from plugin.twitch import Twitch_stream
from plugin.cb import Cb_stream
from recorder.recorder import Recorder

class Streamrecorder:
    def __init__(self):
        self.stream_name = ''
        self.stream_id = ''
        self.stream_type = ''
        self.quality = ''
        self.recording_path = ''
        self.enable_contactsheet = None

    async def run(self):
        title = " ____  _                            ____                        _           \n"
        title += "/ ___|| |_ _ __ ___  __ _ _ __ ___ |  _ \ ___  ___ ___  _ __ __| | ___ _ __ \n"
        title += "\___ \| __| '__/ _ \/ _` | '_ ` _ \| |_) / _ \/ __/ _ \| '__/ _` |/ _ \ '__|\n"
        title += " ___) | |_| | |  __/ (_| | | | | | |  _ <  __/ (_| (_) | | | (_| |  __/ |\n"
        title += "|____/ \__|_|  \___|\__,_|_| |_| |_|_| \_\___|\___\___/|_|  \__,_|\___|_|\n"
        title += '\n'
        start = 'Starting streamrecorder'
        print(title)
        print(start)

        if self.stream_type == 'stream':
            while True:
                channel = Twitch_stream(self.stream_id, self.stream_name, self.stream_type, self.quality)
                status = channel.get_stream_status()
                if status == 'live':
                    print(status)
                    recorder = Recorder()
                    await asyncio.gather(recorder.record(self.recording_path, channel, self.enable_contactsheet))
                elif status == 'offline':
                    print(status)
                    await asyncio.sleep(15)
        elif self.stream_type == 'vod':
            channel = Twitch_stream(self.stream_id, self.stream_name, self.stream_type, self.quality)
            recorder = Recorder()
            await asyncio.gather(recorder.record(self.recording_path, channel, self.enable_contactsheet))
        elif self.stream_type == 'cb':
            while True:
                cb = Cb_stream(self.stream_name)
                status = cb.get_stream_status()
                print(status)
                if status == 'public':
                    print(status)
                    recorder = Recorder()
                    await asyncio.gather(recorder.record(self.recording_path, cb, self.enable_contactsheet))
                elif status == 'offline':
                    print(status)
                    await asyncio.sleep(15)