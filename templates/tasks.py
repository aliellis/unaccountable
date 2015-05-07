import pprint


class Template():
    def __init__(self):
        self.services = {
                         "asana": {
                                    "primaryEmail": "",
                                    "name": {
                                             "givenName": "",
                                             "familyName": "",
                                             "fullName": "",
                                            },
                                    "password": "",
                                    "changePasswordAtNextLogin": "",
                                    "agreedToTerms": "",
                                    },
                         }

    def new_user(self):
        pprint.pprint(self.services["asana"])
