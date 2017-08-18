import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)          # DEBUG INFO WARN ERROR CRITICAL
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)         # DEBUG INFO WARN ERROR CRITICAL
formatter = logging.Formatter('%(levelname)-6s %(filename)s:%(lineno)s:%(funcName)s() %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

import cmd
import os
import sys
import pathlib

import classes.Session
import classes.Model
session = classes.Session.Session()
model = classes.Model.Model()

class InspectModel(cmd.Cmd):
    prompt = '>>'
    intro = "inspectModel version 1.0,\tInspect Keras Model\nType \"help\" or \"?\" to list commands"

    def do_session(self, line):
        session.execute(line)
    def help_session(self):
        session.execute('-h')

    def do_model(self, line):
        #logger.debug('line={}'.format(line))
        model.load(line)
        #if line == 'load':
        #    model.load('dfilename')
        #elif line == 'summary':
        #    model.summary()

    def do_summary(self, line):
        #logger.debug('line={}'.format(line))
        model.summary()

    def do_shell(self, s):
        os.system(s)

    def do_EOF(self, line):
        logger.debug('line={}'.format(line))
        session.execute('save' + ' ' + line)
        #return True
    def do_quit(self, line):
        session.execute(line)
        return True
    def do_exit(self, line):
        session.execute(line)
        return True

    def emptyline(self):
        pass


if __name__ == '__main__':
    InspectModel().cmdloop()
