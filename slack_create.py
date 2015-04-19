import pprint
import json
import urllib2
import yaml


import pprint
import ipdb

import urllib
import urlparse

with open("pk.pem", 'rb') as f:
    private_key = f.read()
    f.close()

config = open("config.yml", "r")
config = yaml.load(config)

AUTH_TOKEN = config["slack_auth_token"]
ENDPOINT = "https://slack.com/api/"


def all_users():
    # slack has a lot of inconsistencies in their json structure, can investigate
    # further but it seems like most are optional, the most reliable form to get
    # real users (not bots) is to return entries with emails
    url = ENDPOINT + "users.list?token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    user_emails = []
    for user in response["members"]:
        if user["deleted"] is False and user["is_bot"] is False:
            user_emails.append(user["profile"]["email"])
    return user_emails

def get_user_info(u_email):
    # although slack has a get_user call, it requires their unique id which can
    # only be found through the users.list method >_>
    url = ENDPOINT + "users.list?token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    for user in response["members"]:
        if user["deleted"] is False and user["is_bot"] is False:
            if u_email in user["profile"]["email"]:
                return user
