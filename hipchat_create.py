import pprint
import json
import urllib2
import yaml

import ipdb

import urllib
import urlparse

config = open("config.yml", "r")
config = yaml.load(config)

AUTH_TOKEN = config["hipchat_auth_token"]
ENDPOINT = "https://api.hipchat.com/v2/"


def all_users():
    url = ENDPOINT + "user?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    response = response["items"]
    return [user["name"] for user in response]


def all_rooms():
    url = ENDPOINT + "room?auth_token=" + AUTH_TOKEN + "&private-room=true"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    response = response["items"]
    return [room["name"] for room in response]


def get_user_info(user):
    url = ENDPOINT + "user/" + user + "?auth_token=" + AUTH_TOKEN
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return json.load(response)


def get_room_members(group):
    url = ENDPOINT + "room/" + group + "?auth_token=" + AUTH_TOKEN
    url = url_fix(url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response = json.load(response)
    return [user["name"] for user in response["participants"]]


def url_fix(s, charset='utf-8'):
    """Grabbed from http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python"""
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
