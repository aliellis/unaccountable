import pprint


class Template():
    def __init__(self):
        self.services = {
                         "google": {
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

                         "hipchat": {
                                     "email": "",
                                     "name": "",
                                     "mention_name": "",
                                     "password": "",
                                    },
                        }

    def new_user(self):
        pprint.pprint(self.services["google"])
