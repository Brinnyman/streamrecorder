import re
import uuid
import requests
import m3u8

class Cb_api:
    def __init__(self):
        self.api_url = 'https://chaturbate.com/get_edge_hls_url_ajax/'

    def get_token(self, url):
        _url_re = re.compile(r"https?://(\w+\.)?chaturbate\.com/(?P<username>\w+)")
        match = _url_re.match(url)
        username = match.group("username")
        CSRFToken = str(uuid.uuid4().hex.upper()[0:32])

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": CSRFToken,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url,
        }

        cookies = {
            "csrftoken": CSRFToken,
        }

        post_data = "room_slug={0}&bandwidth=high".format(username)
        return headers, cookies, post_data


    def get_stream(self, url):
        headers, cookies, post_data = self.get_token(url)
        r = requests.post(self.api_url, headers=headers, cookies=cookies, data=post_data)
        m3u8_obj = m3u8.loads(r.text)
        return m3u8_obj

    def get_stream_info(self, url):
        headers, cookies, post_data = self.get_token(url)
        r = requests.post(self.api_url, headers=headers, cookies=cookies, data=post_data)
        json = r.json()
        return json

class Cb_stream:
    def __init__(self, name):
        self.name = name
        self.url = 'https://chaturbate.com/' + name

    def get_stream_url(self):
        return self.url

    def get_stream_name(self):
        return self.name

    def get_stream_uri(self):
        stream = Cb_api()
        stream_uri_dictionary = stream.get_stream_info(self.get_stream_url())
        return stream_uri_dictionary['url']

    def get_stream_info(self):
        stream = Cb_api()
        stream_info = stream.get_stream_info(self.get_stream_url())
        return stream_info

    def get_stream_status(self):
        stream = Cb_api()
        stream_info = stream.get_stream_info(self.get_stream_url())
        if (stream_info["success"] is True and stream_info["room_status"] == "public" and stream_info["url"]):
            return stream_info["room_status"]
        else:
            return 'offline'
