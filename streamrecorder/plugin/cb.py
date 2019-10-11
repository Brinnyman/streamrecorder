import re
import uuid
import requests
import m3u8
from collections import OrderedDict


class CbApi:
    def __init__(self):
        self.api_url = 'https://chaturbate.com/get_edge_hls_url_ajax/'
        self.playlist = ''
        self.base_uri = ''

    def get_token(self, url):
        _url_re = re.compile(r"https?://(\w+\.)?chaturbate\.com/(?P<username>\w+)")
        match = _url_re.match(url)
        username = match.group("username")
        csrf_token = str(uuid.uuid4().hex.upper()[0:32])

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-csrf_token": csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url,
        }

        cookies = {
            "csrftoken": csrf_token,
        }

        post_data = "room_slug={0}&bandwidth=high".format(username)
        r = requests.post(self.api_url, headers=headers, cookies=cookies, data=post_data)
        json = r.json()
        self.playlist = json['url']
        self.base_uri = self.playlist.split("playlist.m3u8",1)[0]
        return headers, cookies, post_data

    def get_stream(self, url):
        headers, cookies, post_data = self.get_token(url)
        r = requests.post(self.playlist, headers=headers, cookies=cookies, data=post_data)
        m3u8_obj = m3u8.loads(r.text)
        return m3u8_obj

    def final_sorted_streams(self, uris):
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
            return (stream_weight(s)[0] or
                    (len(uris) == 1 and 1))

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

    def get_stream_uri(self, url, quality):
        m3u8_obj = self.get_stream(url)
        get_stream_uris = {}
        for p in m3u8_obj.playlists:
            uri = self.base_uri + p.uri
            get_stream_uris[str(p.stream_info.resolution[1])] = uri
        final_sorted_streams = self.final_sorted_streams(get_stream_uris)
        if quality == '':
            quality = 'best'

        return [val for key, val in final_sorted_streams.items() if quality in key]

    def get_stream_info(self, url):
        headers, cookies, post_data = self.get_token(url)
        r = requests.post(self.api_url, headers=headers, cookies=cookies, data=post_data)
        json = r.json()
        return json


class CbStream:
    def __init__(self, stream_name, stream_quality):
        self.stream_name = stream_name
        self.url = 'https://chaturbate.com/' + stream_name
        self.stream_quality = stream_quality

    def get_stream_name(self):
        return self.stream_name

    def get_stream_url(self):
        return self.url

    def get_stream_quality(self):
        return self.stream_quality

    def get_stream_uri(self):
        stream = CbApi()
        stream_uri = stream.get_stream_uri(self.get_stream_url(), self.get_stream_quality())
        return stream_uri

    def get_stream_info(self):
        stream = CbApi()
        stream_info = stream.get_stream_info(self.get_stream_url())
        return stream_info

    def get_stream_status(self):
        stream = CbApi()
        stream_info = stream.get_stream_info(self.get_stream_url())
        if stream_info["success"] is True and stream_info["room_status"] == "public" and stream_info["url"]:
            return stream_info["room_status"]
        else:
            return 'offline'
        
