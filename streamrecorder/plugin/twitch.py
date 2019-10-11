import configparser
import os
import requests
import random
import m3u8


class TwitchApi:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config.ini'))
        self.twitch_client_id = self.config['TWITCH']['TWITCH_CLIENT_ID']
        self.usher_token = ''
        self.api_token = ''
        self.twitch_api_url = ''

    def set_tokens(self, stream_type):
        if stream_type == 'stream':
            self.usher_token = 'https://usher.ttvnw.net/api/channel/hls/{stream_id}.m3u8?player=twitchweb&token={token}&sig={sig}&$allow_audio_only=true&allow_source=true&type=any&p={random}'
            self.api_token = 'https://api.twitch.tv/api/channels/{stream_id}/access_token?platform=_'
            self.twitch_api_url = 'https://api.twitch.tv/kraken/streams/{stream_id}'
        elif stream_type == 'vod':
            self.usher_token = 'https://usher.ttvnw.net/vod/{stream_id}.m3u8?player=twitchweb&token={token}&sig={sig}&$allow_audio_only=true&allow_source=true&type=any&p={random}'
            self.api_token = 'https://api.twitch.tv/api/vods/{stream_id}/access_token?platform=_'
            self.twitch_api_url = 'https://api.twitch.tv/kraken/videos/{stream_id}'

    def get_token(self, stream_id):
        url = self.api_token.format(stream_id=stream_id)
        r = requests.get(url, headers={"Client-ID": self.twitch_client_id})
        json = r.json()
        token = json['token']
        sig = json['sig']
        return token, sig

    def get_stream(self, stream_id):
        token, sig = self.get_token(stream_id)
        url = self.usher_token.format(stream_id=stream_id, token=token, sig=sig, random=random.randint(0, 1E7))
        r = requests.get(url, headers={"Client-ID": self.twitch_client_id})
        m3u8_obj = m3u8.loads(r.text)
        return m3u8_obj

    def get_stream_uri(self, stream_id, quality):
        stream_uri_dictionary = self.get_stream(stream_id)
        get_stream_uris = {}
        for p in stream_uri_dictionary.playlists:
            get_stream_uris[p.media[0].name] = p.uri
        uri = [val for key, val in get_stream_uris.items() if quality in key]
        return uri[0]

    def get_stream_info(self, stream_id):
        url = self.twitch_api_url.format(stream_id=stream_id)
        r = requests.get(url, headers={"Client-ID": self.twitch_client_id})
        json = r.json()
        return json


class TwitchStream:
    def __init__(self, stream_id, stream_name, stream_type, stream_quality):
        self.stream_id = stream_id
        self.stream_name = stream_name
        self.stream_type = stream_type
        self.stream_quality = stream_quality

    def get_stream_id(self):
        return self.stream_id

    def get_stream_name(self):
        return self.stream_name

    def get_stream_type(self):
        return self.stream_type

    def get_stream_quality(self):
        return self.stream_quality

    def get_stream_uri(self):
        stream = TwitchApi()
        stream.set_tokens(self.get_stream_type())
        stream_uri = stream.get_stream_uri(self.get_stream_id(), self.get_stream_quality())
        return stream_uri

    def get_stream_info(self):
        stream = TwitchApi()
        stream.set_tokens(self.get_stream_type())
        stream_info = stream.get_stream_info(self.get_stream_id())
        return stream_info

    def get_stream_status(self):
        stream = TwitchApi()
        stream.set_tokens(self.get_stream_type())
        stream_info = stream.get_stream_info(self.get_stream_id())
        if stream_info['stream'] is None:
            return 'offline'
        else:
            return stream_info['stream']['stream_type']
