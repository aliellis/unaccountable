import cmd
import os.path

from prettytable import PrettyTable
from cmd_display import generate_table

import ipdb


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
        print ""
        print Colours.YELLOW + "{}{}".format("-", "~") * 40 + Colours.END
        print ""
        print Colours.GREEN + """Welcome to unaccountable, type 'help' for more information""" 
        print ""
        print "If you have not yet provided a configuration file, type 'configure'" + Colours.END
        print ""
        print Colours.YELLOW + "{}{}".format("-", "~") * 40 + Colours.END
        print ""

    def do_prompt(self, arg):
        self.prompt = arg

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

    def do_list_google_users(self, arg):
        import google_create as gc
        users = dict(Users=gc.all_users())
        print generate_table(users)

    def do_google_user(self, arg):
        import google_create as gc
        print "Enter user email address"
        user = raw_input("> ")
        if gc.get_user_info(user):
            print gc.get_user_info(user)
        else:
            print "Sorry, there is no record of a " + str(user) + " account in gmail"

    def do_list_slack_users(self, arg):
        import slack_create as sc
        users = dict(Users=sc.all_users())
        print generate_table(users)

    def do_slack_user(self, arg):
        import slack_create as sc
        print "Enter user email address"
        user = raw_input("> ")
        if sc.get_user_info(user):
            print sc.get_user_info(user)
        else:
            print "Sorry, there is no record of a " + str(user) + " account in slack"

    def do_list_hipchat_users(self, arg):
        import hipchat_create as hc
        users = dict(Users=hc.all_users())
        print generate_table(users)

    def do_hipchat_user(self, arg):
        import hipchat_create as hc
        print "Enter user email address"
        user = raw_input("> ")
        if hc.get_user_info(user):
            print hc.get_user_info(user)
        else:
            print "Sorry, there is no record of a " + str(user) + " account in hipchat"

    def do_list_user_services(self, arg):
        from global_query import is_user_in
        print "Enter user email address"
        user = raw_input("> ")
        services = ["google", "hipchat", "slack"]
        result = is_user_in(user, services)

        # TODO: refacter table generation to make this less manual
        from prettytable import PrettyTable
        x = PrettyTable()
        col_1= result.values()[0]
        col_2 = result.values()[1]
        col_3 = result.values()[2]
        x.add_column(result.keys()[0], [str(col_1)])
        x.add_column(result.keys()[1], [str(col_2)])
        x.add_column(result.keys()[2], [str(col_3)])
        x.align = 'l'
        print x


if __name__ == "__main__":
    Unaccountable().cmdloop()
