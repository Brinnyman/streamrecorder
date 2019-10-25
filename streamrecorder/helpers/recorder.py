import asyncio


class Recorder:
    def __init__(self, ffmpeg_path):
        self.ffmpeg_path = ffmpeg_path

    async def record(self, uri, output):
        ffmpeg = "{} -i {} -c copy {}".format(self.ffmpeg_path, uri, output)
        proc = await asyncio.create_subprocess_shell(
            ffmpeg, stdout=asyncio.subprocess.PIPE
        )
        await proc.wait()

# TODO KeyboardInterrupt
# TODO Check if 3rd-party programs are installed