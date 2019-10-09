```Shell
usage: streamrecorder [-h] -n name -t type [-i id] [-p path] [-q quality] [-c]

Record a stream

optional arguments:
  -h, --help            show this help message and exit
  -n name, --name name  stream name
  -t type, --type type  stream type
  -i id, --id id        Twitch stream identification
  -p path, --path path  recording path
  -q quality, --quality quality
                        stream quality
  -c, --contact         disable contactsheet generation
```

```Shell
Example:
streamrecorder -n name -t stream -q 720p
```

## Requirements
- ffmpeg
- requests
- m3u8