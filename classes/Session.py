import logging
logger = logging.getLogger()
try:
    import readline
except ImportError:
    logger.info('readline cannot be imported')    
    readline = None
import pathlib
import argparse
import shlex
import sys

class Session:
    def __init__(self):
        self._baseDir = pathlib.Path.home().joinpath('.inspectModel')
        self._sessionDir = self._baseDir.joinpath('session')
        self._sessionDir.mkdir(exist_ok=True, parents=True)
        self._sessionFile = self._sessionDir.joinpath('default')
        self._sessionFile.touch(exist_ok=True)
        if readline:
            self._READLINE_FILE_SIZE = 1000
            self._readlineFile = self._baseDir.joinpath('readlineFile')
            self._readlineFile.touch(exist_ok=True)
            readline.read_history_file('{}'.format(self._readlineFile))

    def _load(self, args):
        logger.debug('args.load={}, self._sessionFile{}'.format(args.load, self._sessionFile))
        self._sessionFile = self._sessionDir.joinpath(args.load)
        logger.debug('args.load={}, self._sessionFile{}'.format(args.load, self._sessionFile))
        #with self._sessionFile.open('r') as rf:
            #wf.write("Hello world")

    def _save(self, args):
        logger.debug('args.save={}'.format(args.save))
        if (not args.save) and (not self._sessionFile):
            return
        if args.save:
            self._sessionFile = args.save
        logger.debug('self._sessionFile={}'.format(self._sessionFile))

        if readline:
            readline.set_history_length(self._READLINE_FILE_SIZE )
            readline.write_history_file('{}'.format(self._readlineFile))

    def _state(self):
        logger.debug('entered state')

    def _clear(self):
        logger.debug('entered clear')

    def execute(self, line):
        logger.debug('line={}, shlex.split(line)={}'.format(line, shlex.split(line)))
        self._sessionP = argparse.ArgumentParser(prog="session", 
            description='Information and operations on the session',
            epilog='Long options can be abbreviated if they are unambiguous in the commandline') 
        self._sessionPGr = self._sessionP.add_mutually_exclusive_group()
        self._sessionPGr.add_argument('--clear', '-c', action='store_true', 
                help='clear the session to the default values')
        self._sessionPGr.add_argument('--state', '-s', action='store_true', 
                help='show the state/status of the session')
        try:
            args = self._sessionP.parse_args(shlex.split(line))
            logger.debug('{}'.format(args))
        except SystemExit:
            return
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise   
        if args.clear:      self._clear()
        elif args.state:    self._state()
        else:               self._state()    
