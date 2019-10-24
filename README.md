## Requirements
- ffmpeg
- requests
- m3u8
- vcsi

## Setup recorder
Create a copy of the `_config.ini` and rename the file to `config.ini`.

```ini
[SETUP]
RECORDING_PATH = path to where the recordings will be saved.

[TWITCH]
TWITCH_CLIENT_ID = twitch client id

[FFMPEG]
FFMPEG_PATH = command or path to where ffmpeg is installed.

[VCSI]
CONTACT_SHEET_EXTENSION = command or path to where vcsi is installed.
```

## Usage

```Shell
usage: streamrecorder [-h] [-u url] [-q quality] [-p path] [-t stream_type] [-c]

optional arguments:
  -h, --help      show this help message and exit
  -u              url
  -q              quality
  -p              path
  -t              stream type
  -c              disable contactsheet
```

```Shell
Example:
python streamrecorder -u https://twitch.tv/lirik -q 720p -t twitch -p ./recording
```