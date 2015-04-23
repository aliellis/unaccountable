import requests
import json


class Asana():
    def __init__(self, config):
        self.endpoint = "https://app.asana.com/api/1.0/"
        self.auth_token = config["asana_auth_token"]

    def all_users(self):
        url = "{}users".format(self.endpoint)
        auth = self.auth_token
        r = requests.get(url, auth=(auth, ""))
        res = json.loads(r.text)
        return [res["name"] for res in res["data"]]
