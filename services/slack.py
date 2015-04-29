import json
import urllib2
import yaml

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
