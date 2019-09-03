from helpers.xmlHttpRequest import XmlHttpRequest

xhr = XmlHttpRequest()


class TwitchAPI:
    # connect to twitch with kraken
    def twitch_api(self, api, client_id):
        return xhr.get_response(api, client_id)

    # return stream information 
    def get_stream_information(self, channel, client_id):
        return self.twitch_api('https://api.twitch.tv/kraken/streams/' + channel, client_id)

    # return stream status
    def get_stream_status(self, channel, client_id):
        info = self.get_stream_information(channel, client_id)
        status = None
        if info['stream'] is None:
            status = 0
        elif info['stream']['stream_type'] == 'live':
            status = 1

        return status

    # return vod information 
    def get_vod_information(self, vod_id, client_id):
        return self.twitch_api('https://api.twitch.tv/kraken/videos/' + vod_id, client_id)
