import cmd
import os.path

import google_create as gc
import hipchat_create as hc
import jira_create as jc
import slack_create as jc


class Unaccountable(cmd.Cmd):
    prompt = "unaccountable: "

    def __init__(self):
        cmd.Cmd.__init__(self)
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

    def do_help(self, arg):
        return

    def do_configure(self, arg):
        if os.path.isfile('config.yml'):
            print "'config.yml' already exists, is it ok to overwrite? y/n"
            res = raw_input("> ")
            if res.lower() in ("yes", "y"):
                print "yes?" + str(res)
            elif res.lower() in ("no", "n"):
                print "no?" + str(res)
            elif res.lower() in ("abort", "a"):
                return
            else:
                print "please enter 'y' or 'n', to return to the main menu, type 'abort' or 'a'"

    def do_list_google_users():
        return


if __name__ == "__main__":
    Unaccountable().cmdloop()
