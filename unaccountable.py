import cmd
import os.path


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
        print gc.all_users()

    def do_list_slack_users(self, arg):
        import slack_create as sc
        print sc.all_users()

    def do_list_hipchat_users(self, arg):
        import hipchat_create as hc
        print hc.all_users()


if __name__ == "__main__":
    Unaccountable().cmdloop()
