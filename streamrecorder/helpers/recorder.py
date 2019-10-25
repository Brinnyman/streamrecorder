import asyncio
from helpers.contactsheet import ContactSheet


class Recorder:
    def __init__(self, ffmpeg_path, vcsi_path, recording):
        self.ffmpeg_path = ffmpeg_path
        self.vcsi_path = vcsi_path
        self.uri = recording["uri"]
        self.output = recording["output"]
        self.enable_contactsheet = recording["enable_contactsheet"]

    async def record(self):
        ffmpeg = "{} -i {} -c copy {}".format(self.ffmpeg_path, self.uri, self.output)
        proc = await asyncio.create_subprocess_shell(
            ffmpeg, stdout=asyncio.subprocess.PIPE
        )
        await proc.wait()

        if self.enable_contactsheet:
            contactsheet = ContactSheet(self.vcsi_path)
            contactsheet.create_contact_sheet(self.output)


# TODO KeyboardInterrupt
# TODO Check if 3rd-party programs are installed
