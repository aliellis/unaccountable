import cmd
import os.path

from prettytable import PrettyTable
from cmd_display import generate_table
import pprint


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

    def do_list_google_users(self, arg):
        import google_create as gc
        users = dict(Users=gc.all_users())
        print generate_table(users)

    def do_google_user(self, arg):
        import google_create as gc
        print "Enter user email address"
        user = raw_input("> ")
        if gc.get_user_info(user):
            pprint.pprint(gc.get_user_info(user))
        else:
            print "Sorry, there is no record of a " + str(user) + " account in gmail"

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

    def do_list_slack_users(self, arg):
        import slack_create as sc
        users = dict(Users=sc.all_users())
        print generate_table(users)

    def do_slack_user(self, arg):
        import slack_create as sc
        print "Enter user email address"
        user = raw_input("> ")
        if sc.get_user_info(user):
            pprint.pprint(sc.get_user_info(user))
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
            pprint.pprint(hc.get_user_info(user))
        else:
            print "Sorry, there is no record of a " + str(user) + " account in hipchat"

    def do_list_user_services(self, arg):
        from global_query import is_user_in
        print "Enter user email address"
        user = raw_input("> ")
        services = ["google", "hipchat", "slack"]
        result = is_user_in(user, services)

        # convert values to lists with strings
        for key in result:
            result[key] = [str(result[key])]
        print generate_table(result)

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
