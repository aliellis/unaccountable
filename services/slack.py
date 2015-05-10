import json
import urllib2
import yaml
import pprint

# import urllib
# import urlparse


class Slack():
    def __init__(self, config):
        self.endpoint = "https://slack.com/api/"
        self.auth_token = config["slack_auth_token"]

    def all_users(self):
        # slack has a lot of inconsistencies in their json structure, can investigate
        # further but it seems like most are optional, the most reliable form to get
        # real users (not bots) is to return entries with emails
        url = "{}users.list?token={}".format(self.endpoint, self.auth_token)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        user_emails = []
        for user in response["members"]:
            if user["deleted"] is False and user["is_bot"] is False:
                user_emails.append(user["profile"]["email"])
        return user_emails

    def get_user(self, u_email):
        # although slack has a get_user call, it requires their unique id which can
        # only be found through the users.list method >_>
        url = "{}users.list?token={}".format(self.endpoint, self.auth_token)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        for user in response["members"]:
            if user["deleted"] is False and user["is_bot"] is False:
                if u_email in user["profile"]["email"]:
                    return user

    def is_user_admin(self, u_email):
        try:
            if self.get_user(u_email)["is_admin"] is True:
                return True
        except:
            False

    def all_groups_raw(self):
        url = "{}channels.list?token={}".format(self.endpoint, self.auth_token)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return json.load(response)

    def get_user_groups(self, u_email):
        if self.get_user(u_email)["id"]:
            user_id = self.get_user(u_email)["id"]
            all_groups = self.all_groups_raw()["channels"]
            groups = []

            for group in all_groups:
                if user_id in group["members"]:
                    print group["name"]
                    groups.append(group["name"])

        if groups:
            return groups
        else:
            print "sorry, {} is not in any groups".format(u_email)

    def all_groups(self):
        groups = self.all_groups_raw()
        return [group["name"] for group in groups["channels"]]

    def get_group_id(self, group_name):
        for group in self.all_groups_raw()["channels"]:
            if group_name in group["name"]:
                return group["id"]

    def add_to_group(self, u_email, group):
        if self.get_group_id(group):
            group_id = self.get_group_id(group)
            if self.get_user(u_email)["id"]:
                user_id = self.get_user(u_email)["id"]
                url = "{}channels.invite?token={}&channel={}&user={}".format(self.endpoint, self.auth_token, group_id, user_id)
                print "sending request for {} to join {}".format(u_email, group)
                urllib2.Request(url)
                print "request sent"

    def get_members_raw(self, group):
        all_channels = self.all_groups_raw()["channels"]
        for channel in all_channels:
            if channel["name"] == group:
                url = "{}channels.info?token={}&channel={}".format(self.endpoint, self.auth_token, channel["id"])
                request = urllib2.Request(url)
                response = urllib2.urlopen(request)
                return json.load(response)

    def get_user_with_id(self, u_id):
        url = "{}users.info?token={}&user={}".format(self.endpoint, self.auth_token, u_id)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return json.load(response)

    def get_members(self, group):
        raw = self.get_members_raw(group)
        member_ids = raw["channel"]["members"]
        u_emails = []
        for u_id in member_ids:
            user = self.get_user_with_id(u_id)["user"]
            if user["deleted"] is False and user["is_bot"] is False:
                u_emails.append(self.get_user_with_id(u_id)["user"]["profile"]["email"])
        return u_emails
