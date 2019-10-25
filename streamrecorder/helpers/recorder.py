import asyncio
from helpers.contactsheet import ContactSheet


class Recorder:
    def __init__(self, ffmpeg_path, vcsi_path):
        self.ffmpeg_path = ffmpeg_path
        self.vcsi_path = vcsi_path

    async def record(self, uri, output, enable_contactsheet):
        ffmpeg = "{} -i {} -c copy {}".format(self.ffmpeg_path, uri, output)
        proc = await asyncio.create_subprocess_shell(
            ffmpeg, stdout=asyncio.subprocess.PIPE
        )
        await proc.wait()

        if enable_contactsheet:
            contactsheet = ContactSheet(self.vcsi_path)
            contactsheet.create_contact_sheet(output)

# TODO KeyboardInterrupt
# TODO Check if 3rd-party programs are installed
