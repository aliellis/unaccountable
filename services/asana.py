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

    def all_workspaces(self):
        url = "{}workspaces".format(self.endpoint)
        auth = self.auth_token
        r = requests.get(url, auth=(auth, ""))
        return json.loads(r.text)

    def get_task_ids(self, user):
        workspace_id = self.all_workspaces()["data"][0]["id"]
        url = "{}tasks?workspace={}&assignee={}".format(self.endpoint, workspace_id, user)
        auth = self.auth_token
        r = requests.get(url, auth=(auth, ""))
        return json.loads(r.text)

    def get_task_info(self, task_id):
        url = "{}tasks/{}".format(self.endpoint, task_id)
        auth = self.auth_token
        r = requests.get(url, auth=(auth, ""))
        return json.loads(r.text)

    def get_teams(self):
        workspace_id = self.all_workspaces()["data"][0]["id"]
        url = "{}organizations/{}/teams".format(self.endpoint, workspace_id)
        auth = self.auth_token
        r = requests.get(url, auth=(auth, ""))
        return json.loads(r.text)


        # https://app.asana.com/api/1.0/organizations/13523/teams
