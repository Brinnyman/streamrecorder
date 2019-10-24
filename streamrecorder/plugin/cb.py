import re
import uuid
import requests
import m3u8
from collections import OrderedDict
from urllib.parse import urlparse

_url_re = re.compile(r"https?://(\w+\.)?chaturbate\.com/(?P<username>\w+)")


class CbAPI:
    def __init__(self):
        pass

    def call(self, path, **extra_params):
        url = "https://chaturbate.com/get_edge_hls_url_ajax/"
        csrf_token = str(uuid.uuid4().hex.upper()[0:32])
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-csrf_token": csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url,
        }
        cookies = {"csrftoken": csrf_token}
        r = requests.post(url, headers=headers, cookies=cookies, data=path)
        json = r.json()
        return json

    def access_token(self, asset, **extra_params):
        return self.call("room_slug={0}&bandwidth=high".format(asset), **extra_params)


class CbStream:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        match = _url_re.match(self.stream_url).groupdict()
        parsed = urlparse(self.stream_url)
        self._channel = None
        self._channel = match.get("username") and match.get("username").lower()
        self.quality = ""
        self.api = CbAPI()

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    def _access_token(self):
        value = self.channel
        json = self.api.access_token(value)
        return json

    def _get_hls_streams(self):
        quality = self.quality
        get_stream_uris = {}
        json = self._access_token()
        url = json["url"]
        base_uri = json["url"].split("playlist.m3u8", 1)[0]
        r = requests.get(url)
        if r.status_code != 200:
            return get_stream_uris
        else:
            m3u8_obj = m3u8.loads(r.text)
            for p in m3u8_obj.playlists:
                uri = base_uri + p.uri
                get_stream_uris[str(p.stream_info.resolution[1])] = uri
            final_sorted_streams = self._final_sorted_streams(get_stream_uris)
            uri = [val for key, val in final_sorted_streams.items() if quality in key]
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
        return self._get_hls_streams()
