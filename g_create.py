import time
import ipdb
import httplib2
import json
import yaml
import pprint

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import SignedJwtAssertionCredentials

with open("pk.pem", 'rb') as f:
    private_key = f.read()
    f.close()

config = open("config.yml", "r")
config = yaml.load(config)

SERVICE_ACCOUNT_EMAIL = config["service_account_email"]
SERVICE_USER_EMAIL = config["service_user_email"]
SERVICE_DOMAIN = config["domain"]

http = httplib2.Http()
credentials = SignedJwtAssertionCredentials(
                                            SERVICE_ACCOUNT_EMAIL,
                                            private_key,
                                            scope=["https://www.googleapis.com/auth/admin.directory.group",
                                                   "https://www.googleapis.com/auth/admin.directory.user"],
                                            sub=SERVICE_USER_EMAIL
                                           )

http = credentials.authorize(http)

service = build('admin', 'directory_v1', http= http)

def all_groups():
    """
    list all email groups
    """
    r = service.groups().list(domain= SERVICE_DOMAIN).execute()
    groups = []
    for group in r["groups"]:
        groups.append(group["email"])
    return groups

def all_users():
    """
    list all user emails
    """
    r = service.users().list(domain= SERVICE_DOMAIN).execute()
    users = []
    for user in r["users"]:
        users.append(user["primaryEmail"])
    return users

def all_user_emails():
    """
    lists all user emails, including aliases
    """
    r = service.users().list(domain= SERVICE_DOMAIN).execute()
    emails = []
    for user in r["users"]:
        for key in user["emails"]:
            emails.append(key.values()[-1].lower())
    return set(emails)

def get_user_info(user):
    """
    - user: string, user email
    """
    r = service.users().get(userKey=user).execute()
    return r

def get_group_members(group):
    """
    - group: string, group email
    """
    r = service.members().list(groupKey=group).execute()
    members = r["members"]
    member_list = [user["email"] for user in members]
    return member_list

def generate_user_template(user, domain_name, pass):
    """
    generates user template json necesssary to create a new user account
    - user: string, user's first and last name separated by whitespace
    - domain_name: string, email domain, e.g 'greatemail.com'
    - pass: string, default password for email account
    """
    json = {
            "primaryEmail": user.split()[0].lower() + domain_name,
            "name": {
                     "givenName": user.split()[0],
                     "familyName": user.split()[1],
                     "fullName": user
                    },
            "password": 'fakepassword',
            "changePasswordAtNextLogin": True,
            "agreedToTerms": False
            }
    return json

def add_aliases(user, aliases):
    """
    add aliases to an existing user, not possible at account creation
    - user: string, user email
    - aliases: list, aliases to be added
    """
    for als in aliases:
        service.users().aliases().insert(userKey=user, body={"alias": als}).execute()

def create_user(user, group, domain_name):
    """
    creates a user account, along with firstnamelastname@[domain_name] and
    firstname.lastname@[domain_name] aliases (if available) and adds them to a
    default group
    - user: string, user to be created, first name and last name separated by
    whitespace
    - group: list, groups user to be added to
    - domain_name: string, email domain, e.g 'greatemail.com'
    """
    user_settings = generate_user_template(user)
    create_user = service.users().insert(body=user_settings)

    desired_aliases = generate_aliases(user)
    valid_aliases = [validate_email(email, all_user_emails()) for email in desired_aliases if validate_email(email, all_user_emails()) is not None]

    create_user.execute()
    # New accounts do not appear immediately, sleeping gives time for it to appear
    # for the alias generation
    print "user created, sleeping for 5 seconds...
    time.sleep(5)
    print str(user) + "created"
    print "adding aliases..."
    add_aliases(user.split()[0].lower() + "@skimlinks.com", valid_aliases)
    print "aliases created"
    print "account creation finished, printing results"
    pprint.pprint(get_user_info(user.split()[0].lower() + domain_name))

# API doesn't let you set aliases at creation so you need to add them later
def generate_aliases(user, domain_name):
    """
    generates default aliases for new users
    - user: string, user's first and last name separated by white space
    - domain_name: string, email domain, e.g 'greatemail.com'
    """
    user = user.lower().split()
    aliases = [
               user[0] + "." + user[1] + domain_name,
               user[0] + user[1] + domain_name
              ]
    return aliases

def validate_email(email, unavailable_emails):
    """
    checks to see if email is available
    - email: string, email you wish to be added
    - unavailable_emails: list, emails that are unavailable
    """
    if email not in unavailable_emails:
        return email

def add_to_group(email, group):
    r = service.users().groups()
    return
