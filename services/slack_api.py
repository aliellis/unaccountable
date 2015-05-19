class SlackAPI():
    def __init__(self, config):
        self.endpoint = "https://slack.com/api/"
        self.auth_token = config["slack_auth_token"]

    def constructor(self, method, action):
        return "{}{}.{}?token={}".format(
                    self.endpoint, method, action, self.auth_token)

    def generate_urls(self, method, actions):
        root_urls = {}
        for i in actions:
            root_urls[i] = self.constructor(method, i)
        return root_urls

    def add_params(self, action, urls, params=None):
        if params:
            for i in params:
                urls[action] += "&{}={}".format(i, params[i])
            return urls[action]
        else:
            return urls[action]

    def channels(self, action, params=None):
        actions = ["list", "create", "history", "info", "invite", "join",
                   "kick"]
        urls = self.generate_urls("channels", actions)
        return self.add_params(action, urls, params)

    def users(self, action, params=None):
        actions = ["getPresence", "info", "list"]
        urls = self.generate_urls("users", actions)
        return self.add_params(action, urls, params)

    def chat(self, action, params=None):
        actions = ["delete", "postMessage", "update"]
        urls = self.generate_urls("chat", actions)
        return self.add_params(action, urls, params)

    def groups(self, action, params=None):
        actions = ["close", "create", "history", "info", "invite", "kick",
                   "leave", "list"]
        urls = self.generate_urls("groups", actions)
        return self.add_params(action, urls, params)
