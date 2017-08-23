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
import pickle 

class Session:
    def __init__(self):
        self._baseDir = pathlib.Path.home().joinpath('.interactKerasModel')
        self._sessionDir = self._baseDir.joinpath('session')
        self._sessionDir.mkdir(exist_ok=True, parents=True)
        self._sessionFile = self._sessionDir.joinpath('settings')
        self._sessionFile.touch(exist_ok=True)
        self._instanceList = []
        self._settings = {}
        if readline:
            self._READLINE_FILE_SIZE = 1000
            self._readlineFile = self._baseDir.joinpath('readlineFile')
            self._readlineFile.touch(exist_ok=True)
            readline.read_history_file('{}'.format(self._readlineFile))

    def load(self, instanceList):
        self._instanceList = instanceList
        if self._sessionFile.stat().st_size:
            with self._sessionFile.open('rb') as rf:
                self._settings = pickle.load(rf)
                logger.debug('self._settings={}'.format(self._settings))
            try:    
                for instance in self._instanceList:
                    instance.load(self._settings)
            except:
                print('Saved settings file is corrupted. Loading default settings instead')
                self. _default()
        else:
            self._default()

    def save(self):
        self._settings = {}
        for instance in self._instanceList:
            instance.save(self._settings)
        logger.debug('self._settings={}'.format(self._settings))
        with self._sessionFile.open('wb') as wf:
            pickle.dump(self._settings, wf)

        if readline:
            readline.set_history_length(self._READLINE_FILE_SIZE )
            readline.write_history_file('{}'.format(self._readlineFile))
        print('Session settings saved')

    def _default(self): 
        for instance in self._instanceList:
            instance.default()

    def _state(self): 
        for instance in self._instanceList:
            instance.state()

    def execute(self, line):
        logger.debug('line={}, shlex.split(line)={}'.format(line, shlex.split(line)))
        self._sessionP = argparse.ArgumentParser(prog="session", 
            description='Information and operations on the session',
            epilog='Long options can be abbreviated if they are unambiguous in the commandline') 
        self._sessionPGr = self._sessionP.add_mutually_exclusive_group()
        self._sessionPGr.add_argument('--default', '-d', action='store_true', 
                help='clear the session with the default values')
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
        if args.default:    self._default()
        elif args.state:    self._state()
        else:               self._state()    
