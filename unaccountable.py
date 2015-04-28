import cmd
import os.path

from prettytable import PrettyTable
from cmd_display import generate_table
import pprint
import yaml

from services.hipchat import Hipchat
from services.slack import Slack
from services.google import Google
from services.asana import Asana
from global_query import MultiQuery


class Colours:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[31m'
    END = '\033[0m'


class Unaccountable(cmd.Cmd):
    prompt = "unaccountable: "

    def __init__(self):
        cmd.Cmd.__init__(self)

        config = open("config.yml", "r")
        config = yaml.load(config)

        # TODO: we should probably auto load these
        self.services = {
            "hipchat": Hipchat(config),
            "slack": Slack(config),
            "google": Google(config),
            "asana": Asana(config)
        }

        self.multi_q = MultiQuery(config)

        print ""
        print "{}{}".format("-", "~") * 40
        print ""
        print """Welcome to unaccountable, type 'help' for more information"""
        print ""
        print "If you have not yet provided a configuration file, type 'configure'"
        print ""
        print "{}{}".format("-", "~") * 40
        print ""

    def do_prompt(self, arg):
        self.prompt = arg

    def do_get_users(self, arg):
        cmds = arg.split()
        if len(cmds) == 0 or cmds[0] not in self.services:
            print("Please specify a valid service")
            return

        service = self.services[cmds[0]]
        users = {"Users": service.all_users()}
        print(generate_table(users))

    def do_get_user(self, arg):
        cmds = arg.split()
        if len(cmds) == 0:
            print("Please specify a valid service or email address")
            return

        elif "@" in cmds[0]:
            res = self.multi_q.is_user(cmds[0])

            # convert values to lists with strings, move this out to table_helpers
            for k in res:
                res[k] = [str(res[k])]
            print generate_table(res)

        # maybe check for 2 more args to support search by name?

        elif cmds[0] not in self.services:
            print("Please specify a valid service")

        else:
            service = self.services[cmds[0]]
            if len(cmds) > 1:
                pprint.pprint(service.get_user(cmds[1]))
            else:
                user = raw_input("Please enter a valid email address: ")
                pprint.pprint(service.get_user(user))

    def do_create_user(self, arg):
        cmds = arg.split()
        if len(cmds) == 0 or cmds[0] != "google" or "hipchat":
            print("Please specify a valid service")
            return

        service = self.services[cmds[0]]

    def do_configure(self, arg):
        # TODO: clean this up a little, ensure it writes strings as strings
        # and ints as ints
        from generate_config import generate_config

        if os.path.isfile('config.yml'):
            print "'config.yml' already exists, is it ok to overwrite? y/n"
            res = raw_input("> ")
            if res.lower() in ("yes", "y"):
                generate_config()
                print "overwritten config.yml"
            elif res.lower() in ("no", "n"):
                return
            elif res.lower() in ("abort", "a"):
                return
            else:
                print "please enter 'y' or 'n', to return to the main menu, type 'abort' or 'a'"
        else:
            generate_config()
            print "config.yml created"

    # Can combine all of these list and get_user_info functions

    def do_edit_user(self, arg):
        print "Which service would you like to edit an account for?"
        print "Google, Slack, Hipchat, Jira"
        service = raw_input("> ")
        if service.lower() == "google":
            import google_create as gc

            print "Please enter the user's email address:"
            user_email = raw_input("> ")
            print "Fetching " + user_email + "'s details..."
            if gc.get_user_info(user_email):
                pprint.pprint(gc.get_user_info(user_email))
            else:
                print "Sorry, there is no record of a " + str(user) + " account in google"

        elif service.lower() == "slack":
            import slack_create as sc

            print "Please enter the user's email address:"
            user_email = raw_input("> ")
            print "Fetching " + user_email + "'s details..."
            if sc.get_user_info(user_email):
                pprint.pprint(sc.get_user_info(user_email))
            else:
                print "Sorry, there is no record of a " + str(user) + " account in slack"

        elif service.lower() == "hipchat":
            import hipchat_create as hc

            print "Please enter the user's email address:"
            user_email = raw_input("> ")
            print "Fetching " + user_email + "'s details..."
            if hc.get_user_info(user_email):
                pprint.pprint(hc.get_user_info(user_email))
            else:
                print "Sorry, there is no record of a " + str(user) + " account in hipchat"

    def do_create_user(self, arg):
        print "Which service would you like to create an account for?"
        print "Google, Slack, Hipchat, Jira"
        service = raw_input("> ")
        if service.lower() == "google":
            import google_create as gc

            print "Would you like a user set up with default parameters, or custom?"
            choice = raw_input("> ")
            if choice.lower() == "default":
                print "Please enter the user's first and last name:"
                user_name = raw_input("> ")
                gc.create_user(user_name)
            elif choice.lower() == "custom":
                return
            else:
                print "Error: please enter a valid service."

        elif service.lower() == "slack":
            print "Slack does not currently support account creation features via their API :("

        elif service.lower() == "hipchat":
            return

        elif service.lower() == "jira":
            return

    # def do_list_user_services(self, arg):
    #     from global_query import is_user_in
    #     print "Enter user email address"
    #     user = raw_input("> ")
    #     services = ["google", "hipchat", "slack"]
    #     result = is_user_in(user, services)
    # 
    #     # convert values to lists with strings
    #     for key in result:
    #         result[key] = [str(result[key])]
    #     print generate_table(result)

    def do_get_tasks(self, arg):
        cmds = arg.split()
        if len(cmds) == 0:
            print("Please specify a user email")
            return
        else:
            task_ids = [task_id["id"] for task_id in self.services["asana"].get_task_ids(cmds[0])["data"]]
            pprint.pprint([self.services["asana"].get_task_info(t)["data"] for t in task_ids])

    def do_get_teams(self, arg):
        print [team["name"] for team in self.services["asana"].get_teams()["data"]]

    def do_is_admin(self, arg):
        from global_query import is_user_admin_in
        print "Enter user email address"
        user = raw_input("> ")
        services = ["google", "hipchat", "slack"]
        result = is_user_admin_in(user, services)

        # convert values to lists with strings
        for key in result:
            result[key] = [str(result[key])]
        print generate_table(result)


if __name__ == "__main__":
    Unaccountable().cmdloop()
