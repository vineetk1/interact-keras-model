'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)           # DEBUG INFO WARN ERROR CRITICAL
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)         # DEBUG INFO WARN ERROR CRITICAL
formatter = logging.Formatter('%(levelname)-6s %(filename)s:%(lineno)s:%(funcName)s(): %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

import cmd
import os

import classes.Session
import classes.Model

session = classes.Session.Session()
model = classes.Model.Model()
instanceList = [model]
session.settingsLoad(instanceList)

class InteractModel(cmd.Cmd):
    prompt = '>>'
    intro = "interactKerasModel version 0.7.0, Copyright (C) 2017, Interact with Keras based model. GPL-3.0+ open-source license.\nType \"help\" or \"?\" to list commands"

    def do_session(self, line):
        session.execute(line)
    def help_session(self):
        session.execute('-h')

    def do_model(self, line):
        model.execute(line)
    def help_model(self):
        model.execute('-h')

    def do_shell(self, s):
        os.system(s)
    def help_shell(self):
        print('usage: !\nUse \"!\" as escape character to run shell commands')

    def emptyline(self):
        pass

    def do_EOF(self, line):
        session.settingsSave()
        return True
    def help_EOF(self):
        print('usage: EOF\nSave session settings and exit the program')
    def do_quit(self, line):
        session.settingsSave()
        return True
    def help_quit(self):
        print('usage: quit\nSave session settings and exit the program')
    def do_exit(self, line):
        session.settingsSave()
        return True
    def help_exit(self):
        print('usage: exit\nSave session settings and exit the program')

if __name__ == '__main__':
    InteractModel().cmdloop()
