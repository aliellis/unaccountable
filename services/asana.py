import requests
import json
import pprint


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

    def get_user(self, user):
        url = "{}users/{}".format(self.endpoint, user)
        auth = self.auth_token
        try:
            requests.get(url, auth=(auth, ""))
            return json.loads(requests.get(url, auth=(auth, "")).text)["data"]
        except:
            return False

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

    def get_all_team_members(self):
        all_teams = self.get_teams()["data"]
        team_members = {}
        for team in all_teams:
            url = "{}teams/{}/users".format(self.endpoint, team["id"])
            auth = self.auth_token
            r = requests.get(url, auth=(auth, ""))
            team_members[team["name"]] = json.loads(r.text)["data"]
        return team_members

    def get_members(self, group):
        team_members = self.get_all_team_members()
        groups = []
        if group in team_members:
            group_ids = [user["id"] for user in team_members[group]]
            for g_id in group_ids:
                groups.append(self.get_user(g_id)["email"])
        else:
            print "sorry, {} does not exist".format(group)

        # return

    # def get_team_members(self, team_id):
    #     url = "{}teams/{}/users".format(self.endpoint, team_id)
    #     auth = self.auth_token
    #     r = requests.get(url, auth=(auth, ""))
    #     return json.loads(r.text)

    def get_user_groups(self, user):
        groups = []

        print "getting user id"
        if self.get_user(user):
            user_id = self.get_user(user)["id"]

            print "fetching team data"
            all_teams = self.get_teams()["data"]

            print "querying teams for members"
            for team in all_teams:
                url = "{}teams/{}/users".format(self.endpoint, team["id"])
                auth = self.auth_token
                r = requests.get(url, auth=(auth, ""))
                team["members"] = [member["id"] for member in json.loads(r.text)["data"]]

            print "querying teams for user id"
            for team in all_teams:
                if user_id in team["members"]:
                    groups.append(team["name"])

        if groups:
            return groups
        else:
            print "sorry, {} is not a part of any groups".format(user)

    def all_groups(self):
        return [team["name"] for team in self.get_teams()["data"]]
