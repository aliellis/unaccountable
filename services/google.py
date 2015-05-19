import httplib2
import pprint

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

class Google():
    def __init__(self, config):
        self.service_account = config["service_account_email"]
        self.sub_user_email = config["service_user_email"]
        self.domain = config["domain"]
        self.user_pass = config["google_user_pass"]

        with open(config["google_private_key_path"], 'rb') as p_key:
            self.private_key = p_key.read()
            p_key.close()

        http = httplib2.Http()
        """
            Sub account is needed to fulfill these actions
            http://stackoverflow.com/questions/20704925/google-admin-sdk-directory-api-403-python 
        """
        credentials = SignedJwtAssertionCredentials(
                        self.service_account,
                        self.private_key,
                        scope=["https://www.googleapis.com/auth/admin.directory.group",
                               "https://www.googleapis.com/auth/admin.directory.user"],
                        sub=self.sub_user_email
                      )
        http = credentials.authorize(http)
        self.directory_api = build('admin', 'directory_v1', http= http)

    def all_users(self):
        r = self.directory_api.users().list(domain=self.domain, maxResults=500).execute()
        users = []
        for user in r["users"]:
            users.append(user["primaryEmail"])
        return users

    def get_user(self, user):
        r = self.directory_api.users().get(userKey=user)
        try:
            return r.execute()
        except:
            return False

    def is_user_admin(self, user):
        try:
            if (self.get_user(user)["isAdmin"] | self.get_user(user)["isDelegatedAdmin"]):
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

        template = {
                    "primaryEmail": email,
                    "name": {
                             "givenName": user.split()[0],
                             "familyName": user.split()[1],
                             "fullName": user,
                            },
                    "password": pw,
                    "changePasswordAtNextLogin": True,
                    "agreedToTerms": False
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
                    "primaryEmail": user.split()[0].lower() + "@" + self.domain,
                    "name": {
                             "givenName": user.split()[0],
                             "familyName": user.split()[1],
                             "fullName": user
                            },
                    "password": self.user_pass,
                    "changePasswordAtNextLogin": True,
                    "agreedToTerms": False
                   }
        return template

    def create_user(self, user):
        print "ensuring email address is not already taken"

        desired = user["primaryEmail"]
        invalid = self.all_user_emails()
        if self.validate_email(desired, invalid):
            print "creating user based off this template"
            print ""
            pprint.pprint(user)
            print ""
            print "creating user"
            self.directory_api.users().insert(body=user).execute()
            print "user created"
        else:
            print "email address is taken, exiting..."

    # def create_user(self, user):
    #     print "Generating default aliases"
    #     desired_aliases = generate_aliases(user)
    #     print "Validating aliases"
    #     valid_aliases = [validate_email(email, all_user_emails()) for email in desired_aliases if validate_email(email, all_user_emails()) is not None]
    #     create_user.execute()
    # 
    #     # New accounts do not appear immediately
    #     print "User created, sleeping for 5 seconds..."
    #     time.sleep(5)
    #     print str(user) + "created"
    #     print "Adding aliases..."
    #     add_aliases(user.split()[0].lower() + "@" + self.domain, valid_aliases)
    #     print "Aliases created"
    #     print "Account creation finished, printing results"
    #     pprint.pprint(get_user_info(user.split()[0].lower() + "@" + self.domain))

    def validate_email(self, email, unavailable_emails):
        """
        checks to see if email is available
        - email: string, email you wish to be added
        - unavailable_emails: list, emails that are unavailable
        """
        if email not in unavailable_emails:
            return email

    def all_user_emails(self):
        """
        lists all user emails, including aliases
        """
        r = self.directory_api.users().list(domain=self.domain, maxResults=500).execute()
        emails = []
        for user in r["users"]:
            for key in user["emails"]:
                emails.append(key.values()[-1].lower())
        return set(emails)

    # API doesn't let you set aliases at creation so you need to add them later
    def generate_aliases(self, user):
        """
        generates default aliases for new users
        - user: string, user's first and last name separated by white space
        - domain_name: string, email domain, e.g 'greatemail.com'
        """
        domain_name = self.domain
        user = user.lower().split()
        aliases = [
                   user[0] + "." + user[1] + "@" + domain_name,
                   user[0] + user[1] + "@" + domain_name
                  ]
        return aliases

    def add_aliases(self, user, aliases):
        """
        add aliases to an existing user, not possible at account creation
        - user: string, user email
        - aliases: list, aliases to be added
        """
        for als in aliases:
            service.users().aliases().insert(userKey=user, body={"alias": als}).execute()

    def all_groups(self):
        req = self.directory_api.groups().list(domain=self.domain, maxResults=500).execute()

        page_token = ""
        groups = []

        for group in req["groups"]:
            groups.append(group["email"])

        if req["nextPageToken"]:
            page_token = req["nextPageToken"]

        while page_token:
            req2 = self.directory_api.groups().list(domain=self.domain, maxResults=500, pageToken=page_token).execute()
            for group in req2["groups"]:
                groups.append(group["email"])
            page_token = ""
            if "nextPageToken" in req2:
                page_token = req2["nextPageToken"]

        else:
            return groups

    def get_user_groups_raw(self, user):
        return self.directory_api.groups().list(domain=self.domain, userKey=user).execute()

    def get_user_groups(self, user):
        req = self.directory_api.groups().list(domain=self.domain, userKey=user).execute()
        return [group["email"] for group in req["groups"]]

    def add_to_group(self, user, group):
        template = {"email": user}
        self.directory_api.members().insert(body=template, groupKey=group).execute()

    def remove_from_group(self, user, group):
        template = {"email": user}
        self.directory_api.members().delete(groupKey=group, memberKey=user).execute()

    def get_members_raw(self, group):
        return self.directory_api.members().list(groupKey=group).execute()

    def get_members(self, group):
        return [user["email"] for user in self.get_members_raw(group)["members"]]
