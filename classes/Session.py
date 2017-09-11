'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
'''
Commands specific to the session
'''
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
        _baseDir = pathlib.Path.home().joinpath('.interactKerasModel')
        _sessionDir = _baseDir.joinpath('session')
        _sessionDir.mkdir(exist_ok=True, parents=True)
        self._sessionFile = _sessionDir.joinpath('settings')
        self._sessionFile.touch(exist_ok=True)
        if readline:
            self._READLINE_FILE_SIZE = 1000
            self._readlineFile = _baseDir.joinpath('readlineFile')
            self._readlineFile.touch(exist_ok=True)
            readline.read_history_file('{}'.format(self._readlineFile))

    def settingsLoad(self, instanceList):
        self._instanceList = instanceList
        if self._sessionFile.stat().st_size:
            with self._sessionFile.open('rb') as rf:
                self._settings = pickle.load(rf)
                logger.debug('self._settings = {}'.format(self._settings))
            try:    
                for instance in self._instanceList:
                    instance.settingsLoad(self._settings)
            except:
                print('Saved settings file is corrupted. Loading default settings instead')
                self. _settingsDefault()
        else:
            self._settingsDefault()

    def settingsSave(self):
        self._settings = {}
        for instance in self._instanceList:
            instance.settingsSave(self._settings)
        logger.debug('self._settings = {}'.format(self._settings))
        with self._sessionFile.open('wb') as wf:
            pickle.dump(self._settings, wf)

        if readline:
            readline.set_history_length(self._READLINE_FILE_SIZE )
            readline.write_history_file('{}'.format(self._readlineFile))
        print('Session settings saved')

    def _settingsDefault(self): 
        for instance in self._instanceList:
            instance.settingsDefault()

    def _settingsState(self): 
        for instance in self._instanceList:
            instance.settingsState()

    def execute(self, _line):
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _sessionP = argparse.ArgumentParser(prog="session", 
            description='Information and operations on the session',
            epilog='Long options can be abbreviated if they are unambiguous in the commandline') 
        _sessionPGr = _sessionP.add_mutually_exclusive_group()
        _sessionPGr.add_argument('--default', '-d', dest='_default', action='store_true', 
                help='clear the session with the default values')
        _sessionPGr.add_argument('--state', '-s', dest='_state',  action='store_true', 
                help='show the state/status of the session')

        try:
            _args = _sessionP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              
        except:             print("Unexpected error: {}".format(sys.exc_info()[0])); raise

        if _args._default:  self._settingsDefault()
        elif _args._state:  self._settingsState()
        else:               pass    
