import requests


class XmlHttpRequest:
    def __init__(self):
        self.directory = ''

    # get_response
    def get_response(self, api, client_id):
        info = None
        r = requests.get(api, headers={"Client-ID": client_id}, timeout=15)
        r.raise_for_status()
        info = r.json()
        return info
