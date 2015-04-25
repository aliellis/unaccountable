
class ValidExtrap(config):
    def __init__(self):
        self.domain = config["domain"]

    # TODO: create a basic name stemmer
    def guess_email(first_name, last_name):
        return [
                "{}@{}".format(first_name, self.domain)
                "{}.{}@{}".format(first_name, last_name, self.domain)
                "{}{}@{}".format(first_name, last_name, self.domain)
               ]
