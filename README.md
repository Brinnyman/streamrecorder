```Shell
usage: streamrecorder [-h] -n name -t type [-i id] [-p path] [-q quality] [-c]

Record a stream

optional arguments:
  -h, --help      show this help message and exit
  -n, --name      stream name
  -t, --type      stream type
  -i, --id        Twitch stream identification
  -p, --path      recording path
  -q, --quality   stream quality
  -c, --contact   disable contactsheet generation
```

```Shell
Example:
python streamrecorder -n lirik -i lirik -t stream -q 720p -p ./recording
```

## Requirements
- ffmpeg
- requests
- m3u8