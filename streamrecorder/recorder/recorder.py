import asyncio
import configparser
import os
import datetime
from helpers.filesystem import Filesystem
from helpers.contactsheet import ContactSheet


class Recorder():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config.ini'))
        self.ffmpeg_path = config['FFMPEG']['FFMPEG_PATH']

    async def record(self, recording_path, channel, enable_contactsheet):
        f = Filesystem(recording_path, channel.get_stream_name())
        f.create_directory()
        filename = f.create_file(datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
        ffmpeg = '{} -i {} -c copy {}.mkv'.format(self.ffmpeg_path, channel.get_stream_uri(), filename)
        proc = await asyncio.create_subprocess_shell(ffmpeg, stdout=asyncio.subprocess.PIPE)
        await proc.wait()

        if enable_contactsheet:
            contactsheet = ContactSheet()
            contactsheet.create_contact_sheet(filename)
