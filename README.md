```Shell
Usage: streamrecorder [options]
Options:
-h, --help        prints this message
-n, --name        streamer channel
-u, --url         stream url
-q, --quality     recording quality, first that is available <720p, 720p60, 1080p, 1080p60, best>. You can override these by providing the quality or pick the default Streamlink settings <best> or <worst>.
-r, --recordpath  recording path
-c, --commands    additional streamlink commands
-t, --type        recording type <twitch, vod, stream, record, play>
-v, --vod         twitch vod id
-i, --info        twitch stream information
```

```Shell
Example:
streamrecorder -n <twitchstreamer> -t twitch -q 720p
streamrecorder -n <twitchstreamer> -t vod -v <vod_id> -q best
streamrecorder -n <name> -u <url> -t stream -q 720p
```

## Requirements
- ffmpeg
- streamlink
- vcsi