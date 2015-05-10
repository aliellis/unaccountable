import json
import urllib2
import urllib
import urlparse
import requests

import pprint
import re

""" NOTE: Due to rate limiting, and the way HipChat handles user info requests,
    it is currently impossible to fetch ALL user data within a reasonable amount
    of time, this is because the 'user?'' call only returns about 1/2 of the 
    actual user information, crucially, most calls require 2 calls to the api,
    one with the user's email to fetch their unique id, and then again with that
    id to return the user's full profile.
"""


class Hipchat():
    def __init__(self, config):
        self.endpoint = "https://api.hipchat.com/v2/"
        self.auth_token = config["hipchat_auth_token"]
        self.user_pass = config["hipchat_user_pass"]
        self.domain = config["domain"]

    # Can probably remove this when we port over to requests
    # Necessary to handle white space in get_user_info requests
    def url_fix(self, s, charset='utf-8'):
        """Grabbed from http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python"""
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    def all_users(self):
        url = self.endpoint + "user?auth_token=" + self.auth_token
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        response = response["items"]
        return [user["name"] for user in response]

    def all_users_raw(self):
        url = "{}user?auth_token={}".format(self.endpoint, self.auth_token)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        return response

    def get_user(self, user):
        url = self.endpoint + "user/" + user + "?auth_token=" + self.auth_token
        request = urllib2.Request(url)
        try:
            urllib2.urlopen(request)
            return json.load(urllib2.urlopen(request))
        except:
            return False

    def is_user_admin(self, user):
        try:
            if self.get_user(user)["is_group_admin"] is True:
                return True
        except:
            return False

    def generate_user_template(self):
        print "Please enter the user's first and last name: "
        user = raw_input("> ")
        template = self.generate_user_template_from_name(user)
        print ""
        pprint.pprint(template)
        print ""
        print "Is this ok? y/n"
        yn = raw_input("> ")
        if yn.lower() == "y":
            return template
        elif yn.lower() == "n":
            print "generating custom template"
            custom_template = self.generate_user_template_interactive(user)
            while custom_template is None:
                custom_template = self.generate_user_template_interactive(user)
            else:
                return custom_template

    def generate_user_template_interactive(self, user):
        print "Please enter the user's default password"
        pw = raw_input("> ")
        print "Please enter the user's email address"
        email = raw_input("> ")
        print "Please enter the user's mention name"
        mention = raw_input("> ")

        template = {
                    "email": email,
                    "name": user,
                    "mention_name": mention,
                    "password": pw,
                   }
        print ""
        pprint.pprint(template)
        print ""
        print "Is this ok? y/n"
        yn = raw_input("> ")
        if yn.lower() == "y":
            return template
        elif yn.lower() == "n":
            return

    def generate_user_template_from_name(self, user):
        template = {
                    "email": user.split()[0].lower() + "@" + self.domain,
                    "name": user,
                    "mention_name": user.split()[0] + user.split()[1][0],
                    "password": self.user_pass
                   }
        return template

    def is_not_duplicate(self, user, field):
        desired = user[field]
        patt = "^({}.*)".format(desired[0].lower())
        regex = re.compile(patt)
        invalid = self.get_similar_acounts(regex)
        if invalid:
            similar = []
            for user_id in invalid:
                similar.append(self.get_user(user_id)[field])
            if desired in similar:
                print "desired field, {} is already in use by another HipChat user, exiting...".format(desired)
                return False
            else:
                return True

    def create_user(self, user):
        print "ensuring email address and mention name is not already taken"

        if self.is_not_duplicate(user, "email") and self.is_not_duplicate(user, "mention_name"):
            print "no duplicates exist, creating account"

            url = "{}user".format(self.endpoint)
            headers = {"Content-type": "application/json"}
            headers["Authorization"] = "Bearer " + self.auth_token
            params = {"auth_token": self.auth_token}

            requests.post(url,
                          params=params,
                          data=json.dumps(user),
                          headers=headers)
            print "user created"

        else:
            print "duplicates exist, exiting..."

    def get_similar_acounts(self, search_p):
        all_users = self.all_users_raw()
        all_names = [account["name"].lower() for account in all_users["items"]]
        possible_matches = []
        for name in all_users["items"]:
            if name["name"]:
                if search_p.match(name["name"].lower()):
                    possible_matches.append(str(name["id"]))
        return possible_matches

    def add_to_group():
        return

    def all_groups(self):
        # get all rooms, this is just syntax to work with main
        url = self.endpoint + "room?auth_token=" + self.auth_token + "&private-room=true"
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        response = response["items"]
        return [room["name"] for room in response]

    def all_groups_raw(self):
        url = self.endpoint + "room?auth_token=" + self.auth_token + "&private-room=true"
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return json.load(response)

    def get_room_members(self, group):
        url = self.endpoint + "room/" + str(group) + "?auth_token=" + self.auth_token
        url = self.url_fix(url)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response = json.load(response)
        return [user["name"] for user in response["participants"]]

    def get_user_groups(self):
        return

    def get_group(self, g_id):
        url = self.endpoint + "group?auth_token=" + self.auth_token + "&id=" + g_id
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return json.load(response)

    def get_members(self, group):
        all_rooms = self.all_groups_raw()["items"]
        for room in all_rooms:
            if group in room["name"].lower():
                return self.get_room_members(room["id"])
