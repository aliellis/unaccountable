import pprint
import json
import urllib2
import yaml


import pprint
import ipdb

import urllib
import urlparse

config = open("config.yml", "r")
config = yaml.load(config)

AUTH_TOKEN = config["slack_auth_token"]
ENDPOINT = "https://slack.com/api/"

def all_users():
    # slack does not require full names, only way to get a comprehensive list 
    # of users is to return email addresses
    url = ENDPOINT + "users.list?token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    user_emails = []
    for user in response["members"]:
        if user["deleted"] is False and user["is_bot"] is False:
            user_emails.append(user["profile"]["email"])
    return user_emails
