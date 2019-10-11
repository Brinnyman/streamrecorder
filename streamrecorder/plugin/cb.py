import re
import uuid
import requests
import m3u8


class CbApi:
    def __init__(self):
        self.api_url = 'https://chaturbate.com/get_edge_hls_url_ajax/'
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

        post_data = "room_slug={0}&bandwidth=low".format(username)
        r = requests.post(self.api_url, headers=headers, cookies=cookies, data=post_data)
        json = r.json()
        self.base_uri = json['url'].split("playlist.m3u8",1)[0]
        return json, headers, cookies, post_data

    def get_stream(self, url):
        json, headers, cookies, post_data = self.get_token(url)
        r = requests.post(json['url'], headers=headers, cookies=cookies, data=post_data)
        m3u8_obj = m3u8.loads(r.text)
        return m3u8_obj

    def get_stream_uri(self, url, quality):
        m3u8_obj = self.get_stream(url)
        get_stream_uris = {}
        for p in m3u8_obj.playlists:
            uri = self.base_uri + p.uri
            get_stream_uris[str(p.stream_info.resolution[1])] = uri
        uri = [val for key, val in get_stream_uris.items() if quality in key]
        return uri[0]

    def get_stream_info(self, url):
        json, headers, cookies, post_data = self.get_token(url)
        r = requests.post(self.api_url, headers=headers, cookies=cookies, data=post_data)
        json = r.json()
        return json


class CbStream:
    def __init__(self, name, quality):
        self.name = name
        self.url = 'https://chaturbate.com/' + name
        self.quality = quality

    def get_stream_name(self):
        return self.name

    def get_stream_url(self):
        return self.url

    def get_stream_quality(self):
        return self.quality

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
