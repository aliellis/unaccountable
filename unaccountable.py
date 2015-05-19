import cmd
import os.path
import time

from prettytable import PrettyTable
from cmd_display import generate_table, table_contents_to_s
from pprint import pprint
import yaml

from services.hipchat import Hipchat
from services.slack import Slack
from services.google import Google
from services.asana import Asana
from global_query import MultiQuery
from validate import validate_service, validate_user, validate_group


class Unaccountable(cmd.Cmd):
    prompt = "unaccountable: "

    def __init__(self):
        cmd.Cmd.__init__(self)

        config = open("config.yml", "r")
        config = yaml.load(config)

        # TODO: auto load these
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
        """ get_users [service] """
        cmds = arg.split()
        if validate_service(cmds[0], ["google", "asana", "slack", "hipchat"]):

            service = self.services[cmds[0]]
            users = {"Users": service.all_users()}
            print(generate_table(users))

    def do_is_admin(self, arg):
        """ is_admin [user] """
        cmds = arg.split()
        if validate_user(cmds[0]):

            res = self.multi_q.is_user_admin(cmds[0])
            print generate_table(table_contents_to_s(res))

    def do_get_groups(self, arg):
        """ get_groups [service] [user] """
        # yes: slack, google, asana,
        cmds = arg.split()
        if len(cmds) == 2:
            service = self.services[cmds[0]]
            user = cmds[1]
            groups = {"Groups": service.get_user_groups(user)}
            print(generate_table(groups))
        else:
            service = self.services[cmds[0]]
            groups = {"Groups": service.all_groups()}
            print(generate_table(groups))

    def do_add_to_group(self, arg):
        """ add_to_group [service] [user] [group] """
        cmds = arg.split()
        if validate_service(cmds[0], ["google", "slack"]):

            service = self.services[cmds[0]]
            user = cmds[1]
            group = cmds[2]

            service.add_to_group(user, group)

    def do_remove_from_group(self, arg):
        """ remove_from_group [service] [user] [group] """
        cmds = arg.split()
        if validate_service(cmds[0], ["google", "slack"]):

            service = self.services[cmds[0]]
            user = cmds[1]
            group = cmds[2]

            print service.remove_from_group(user, group)

    def do_user_manifest(self, arg):
        """ user_manifest [user] """
        # yes: google, slack, hipchat, asana
        cmds = arg.split()
        if validate_user(cmds[0]):

            pprint(self.multi_q.all_priveliges(cmds[0]))

    def do_get_members(self, arg):
        """ get_members [service] [group] """
        cmds = arg.split()
        if validate_service(cmds[0], ["google", "slack", "asana", "hipchat"]):

            service = self.services[cmds[0]]
            cmds.pop(0)
            group = ""
            for i in cmds:
                group += i + " "
            group = group.strip().lower()
            members = {group: service.get_members(group)}
            print generate_table(members)

    def do_get_user(self, arg):
        """ get_user [service] [user] """
        # yes: slack, google, asana, hipchat
        cmds = arg.split()
        if len(cmds) == 2:
            service = self.services[cmds[0]]
            user = cmds[1].lower()
            pprint(service.get_user(user))

        elif "@" in cmds[0]:
            res = self.multi_q.is_user(cmds[0].lower())
            print generate_table(table_contents_to_s(res))

        elif cmds[0] not in self.services:
            print("Please specify a valid service")

        else:
            service = self.services[cmds[0].lower()]
            if len(cmds) > 1:
                pprint(service.get_user(cmds[1].lower()))
            else:
                user = raw_input("Please enter a valid email address: ")
                pprint(service.get_user(user))

    def do_create_user(self, arg):
        """ create_user [service] [user] """
        cmds = arg.split()
        if validate_service(cmds[0], ["google", "hipchat"]):

            service = self.services[cmds[0]]
            template = service.generate_user_template()
            service.create_user(template)

    def do_configure(self, arg):
        """ configure """
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

    # def do_edit_user(self, arg):
    #     print "Which service would you like to edit an account for?"
    #     print "Google, Slack, Hipchat, Jira"
    #     service = raw_input("> ")
    #     if service.lower() == "google":
    #         import google_create as gc
    # 
    #         print "Please enter the user's email address:"
    #         user_email = raw_input("> ")
    #         print "Fetching " + user_email + "'s details..."
    #         if gc.get_user_info(user_email):
    #             pprint(gc.get_user_info(user_email))
    #         else:
    #             print "Sorry, there is no record of a " + str(user) + " account in google"
    # 
    #     elif service.lower() == "slack":
    #         import slack_create as sc
    # 
    #         print "Please enter the user's email address:"
    #         user_email = raw_input("> ")
    #         print "Fetching " + user_email + "'s details..."
    #         if sc.get_user_info(user_email):
    #             pprint(sc.get_user_info(user_email))
    #         else:
    #             print "Sorry, there is no record of a " + str(user) + " account in slack"
    # 
    #     elif service.lower() == "hipchat":
    #         import hipchat_create as hc
    # 
    #         print "Please enter the user's email address:"
    #         user_email = raw_input("> ")
    #         print "Fetching " + user_email + "'s details..."
    #         if hc.get_user_info(user_email):
    #             pprint(hc.get_user_info(user_email))
    #         else:
    #             print "Sorry, there is no record of a " + str(user) + " account in hipchat"


# ------------------------ASANA SPECIFIC CMDS------------------------

    def do_get_tasks(self, arg):
        cmds = arg.split()
        if len(cmds) == 0:
            print("Please specify a user email")
            return
        else:
            task_ids = [task_id["id"] for task_id in self.services["asana"].get_task_ids(cmds[0])["data"]]
            pprint([self.services["asana"].get_task_info(t)["data"] for t in task_ids])

    # def do_get_members(self, arg):
    #     cmds = arg.split()
    #     if len(cmds) == 0:
    #         print("Please specify a Asana team")
    #         return
    #     else:
    #         raw_teams = self.services["asana"].get_teams()["data"]
    #         for team in raw_teams:
    #             if cmds[0] in team["name"]:
    #                 team_id = team["id"]
    # 
    #                 raw_users = self.services["asana"].get_team_members(team_id)["data"]
    #                 print [user["name"] for user in raw_users]


if __name__ == "__main__":
    Unaccountable().cmdloop()
