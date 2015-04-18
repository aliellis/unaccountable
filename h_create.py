import pprint
import json
import urllib2
import yaml

import ipdb

config = open("config.yml", "r")
config = yaml.load(config)

AUTH_TOKEN = config["auth_token"]

url = "https://api.hipchat.com/v2/room?auth_token=" + AUTH_TOKEN

request = urllib2.Request(url)
response = urllib2.urlopen(request)

def all_users():
    url = "https://api.hipchat.com/v2/user?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    response = response["items"]
    return [user["name"] for user in response]

def all_rooms():
    url = "https://api.hipchat.com/v2/room?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    response = response["items"]
    return[room["name"] for room in response]
