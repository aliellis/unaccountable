import pprint
import json
import urllib2
import yaml
import time
from fn_cache import Memoized
import requests
from urllib import urlencode

import ipdb

import urllib
import urlparse

config = open("config.yml", "r")
config = yaml.load(config)

AUTH_TOKEN = config["hipchat_auth_token"]
USER_PW = config["h_user_pw"]
ENDPOINT = "https://api.hipchat.com/v2/"

""" NOTE: Due to rate limiting, and the way HipChat handles user info requests,
    it is currently impossible to fetch ALL user data within a reasonable amount
    of time, this is because the 'user?'' call only returns about 1/2 of the 
    actual user information, crucially, the user's email address 
"""


def all_users():
    # TODO: create a function that you pass 'name', 'email', 'rights', etc 
    # to make this more modular
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
    try:
        urllib2.urlopen(request)
        return json.load(urllib2.urlopen(request))
    except:
        # TODO: handle these exceptions!
        return False


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


def create_user(user_email, user_name, user_mention, pw=None):
    if pw is None:
        pw = USER_PW
    host = "api.hipchat.com"
    url = "https://{0}/v2/user".format(host)
    headers = {'Content-type': 'application/json'}
    headers['Authorization'] = "Bearer " + AUTH_TOKEN
    params = {"auth_token": AUTH_TOKEN}
    payload = {
        'email': user_email,
        'name': user_name,
        'mention_name': user_mention,
        'password': pw
    }
    requests.post(url, params=params, data=json.dumps(payload), headers=headers)
