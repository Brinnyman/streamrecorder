import configparser
import os
import requests
import random
import m3u8
import re
from collections import OrderedDict
from urllib.parse import urlparse
import datetime

_url_re = re.compile(
    r"http(s)?://(?:(?P<subdomain>[\w\-]+)\.)?twitch.tv/(?:videos/(?P<videos_id>\d+)|(?P<channel>[^/]+))(?:/(?P<video_type>[bcv])(?:ideo)?/(?P<video_id>\d+))?"
)


class UsherService(object):
    def init(self):
        pass

    def _create_url(self, endpoint, **extra_params):
        url = "https://usher.ttvnw.net{0}".format(endpoint)
        params = {
            "player": "twitchweb",
            "p": random.randint(0, 1e7),
            "type": "any",
            "allow_source": "true",
            "allow_audio_only": "true",
            "allow_spectre": "false",
        }
        params.update(extra_params)
        r = requests.get(url, params=params)
        # print('usher: ', url)
        # print('usher response url: ', r.url)
        return r.url

    def channel(self, channel, **extra_params):
        return self._create_url(
            "/api/channel/hls/{0}.m3u8".format(channel), **extra_params
        )

    def video(self, video_id, **extra_params):
        return self._create_url("/vod/{0}".format(video_id), **extra_params)


class TwitchAPI:
    def __init__(self):
        self.subdomain = "api"
        self.config = configparser.ConfigParser()
        self.config.read(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "../config.ini")
        )
        self.twitch_client_id = self.config["TWITCH"]["TWITCH_CLIENT_ID"]

    def call(self, path, **extra_params):
        url = "https://{0}.twitch.tv{1}".format(self.subdomain, path)
        params = {
            "player": "twitchweb",
            "p": random.randint(0, 1e7),
            "type": "any",
            "allow_source": "true",
            "allow_audio_only": "true",
            "allow_spectre": "false",
        }
        params.update(extra_params)
        headers = {
            "Accept": "application/vnd.twitchtv.v5+json",
            "Client-ID": self.twitch_client_id,
        }
        # print('api:', url)
        r = requests.get(url, params=params, headers=headers)
        json = r.json()
        # print('api json', json)
        return json

    def access_token(self, endpoint, asset, **extra_params):
        json = self.call(
            "/api/{0}/{1}/access_token?platform=_".format(endpoint, asset),
            **extra_params
        )
        return json["sig"], json["token"]

    def videos(self, video_id, **params):
        return self.call("/kraken/videos/{0}".format(video_id), **params)


class TwitchStream:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        match = _url_re.match(self.stream_url).groupdict()
        parsed = urlparse(self.stream_url)
        self.subdomain = match.get("subdomain")
        self.video_id = None
        self._video_type = None
        self._channel_id = None
        self._channel = None
        self.stream_type = ""
        self.recorded_at = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        self.quality = ""
        self.config = configparser.ConfigParser()
        self.config.read(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "../config.ini")
        )
        self.twitch_client_id = self.config["TWITCH"]["TWITCH_CLIENT_ID"]
        self._channel = match.get("channel") and match.get("channel").lower()
        self.video_type = match.get("video_type")
        if match.get("videos_id"):
            self.video_type = "v"
        self.video_id = match.get("video_id") or match.get("videos_id")
        self.api = TwitchAPI()
        self.usher = UsherService()

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
        self._channel_id = None

    def _access_token(self, stream_type="live"):
        if stream_type == "live":
            endpoint = "channels"
            value = self.channel
        elif stream_type == "video":
            endpoint = "vods"
            value = self.video_id

        sig, token = self.api.access_token(endpoint, value)
        return sig, token

    def _get_hls_streams(self, stream_type="live"):
        quality = self.quality
        get_stream_uris = {}
        if stream_type == "live":
            sig, token = self._access_token(stream_type)
            url = self.usher.channel(self.channel, sig=sig, token=token)
        elif stream_type == "video":
            sig, token = self._access_token(stream_type)
            url = self.usher.video(self.video_id, sig=sig, token=token)

        r = requests.get(url, headers={"Client-ID": self.twitch_client_id})
        if r.status_code != 200:
            return get_stream_uris
        else:
            m3u8_obj = m3u8.loads(r.text)
            for p in m3u8_obj.playlists:
                get_stream_uris[p.media[0].name] = p.uri
            final_sorted_streams = self._final_sorted_streams(get_stream_uris)
            uri = [val for key, val in final_sorted_streams.items() if quality in key]
            print('hls stream uri: ', uri[0])
            return uri[0]

    def _final_sorted_streams(self, uris):
        def stream_weight(stream):
            match = re.match(r"^(\d+)(p)?(\d+)?(\+)?$", stream)

            if match:
                weight = 0
                name_type = match.group(2)

                if name_type == "p":
                    weight += int(match.group(1))

                    if match.group(3):
                        weight += int(match.group(3))

                    if match.group(4) == "+":
                        weight += 1

                    return weight, "pixels"

            return 0, "none"

        def stream_weight_only(s):
            return stream_weight(s)[0] or (len(uris) == 1 and 1)

        stream_names = uris.keys()
        sorted_streams = sorted(stream_names, key=stream_weight_only)
        final_sorted_streams = OrderedDict()

        for stream_name in sorted(uris, key=stream_weight_only):
            final_sorted_streams[stream_name] = uris[stream_name]

        if len(sorted_streams) > 0:
            worst = sorted_streams[0]
            best = sorted_streams[-1]
            final_sorted_streams["worst"] = uris[worst]
            final_sorted_streams["best"] = uris[best]

        return final_sorted_streams

    def _get_streams(self):
        if self.video_id:
            if self.video_type == "v":
                self.stream_type = "video"
                videos = self.api.videos(self.video_type + self.video_id)
                self.channel = videos["channel"]["name"]
                self.recorded_at = videos["recorded_at"]
                return self._get_hls_streams(self.stream_type)
        elif self._channel:
            self.stream_type = "live"
            return self._get_hls_streams(self.stream_type)

# TODO AttributeError: 'NoneType' object has no attribute 'groupdict'
# TODO Double request, channel._get_streams(), create an object with the stream results[name, date, uri]