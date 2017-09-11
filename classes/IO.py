'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
'''
Commands to obtain the outputs of the various layers in the model, for a given input
'''
import logging
logger = logging.getLogger()
import classes.CommonModel as cm
import pathlib
import keras.models
import sys
import argparse
import shlex
import contextlib 

class IO(cm.CommonModel):
    def __init__(self):
        pass

    def _setup(self, _args):
        try: self._infile = super().absPathFile(_args.inFile)
        except: self._inFile = None
        try: self._exptdOutFile = super().absPathFile(_args.exptdOutFile)
        except: self._exptdOutFile = None
        try: self._outFile = super().absPathFile(_args.outFile)
        except: self._outFile = None

    def _run(self, _args):
        logger.debug('got here')

    def settingsLoad(self, _settings):
        try:
            self._infile = _settings['ioInFile']
            self._exptdOutFile = _settings['ioExptdOutFile']
            self._outFile = _settings['ioOutFile']
        except:
            logger.warn('one or more IO files  not in settings = {}; settings file possibly corrupted'.format(
                _settings))
            raise

    def settingsSave(self, _settings):
        _settings['ioInFile'] = self._infile
        _settings['ioExptdOutFile'] = self._exptdOutFile
        _settings['ioOutFile'] = self._outFile

    def settingsDefault(self):
        self._infile = None
        self._exptdOutFile = None
        self._outFile = None

    def settingsState(self):
        print('io input file: {}'.format(self._infile if self._infile else None))
        print('io expected output file: {}'.format(self._exptdOutFile if self._exptdOutFile else None))
        print('io output file: {}'.format(self._outFile if self._outFile else None))

    def execute(self, _line):
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _ioP = argparse.ArgumentParser(prog="io", 
            description='Commands specific to Input and Output of the model',
            epilog='long options can be abbreviated if they are unambiguous in the commandline') 
        _ioPs = _ioP.add_subparsers()

        _ioPsSetup = _ioPs.add_parser('setup', aliases=['se'],
                help='setup the model before running it')
        _ioPsSetup.add_argument('--inFile', '-if', action='store', metavar='fileName',
                help='path of the file that has the inputs to the model')
        _ioPsSetup.add_argument('--exptdOutFile', '-ef', action='store', metavar='fileName',
                help='path of the file that has the expected outputs from the model')
        _ioPsSetup.add_argument('--outFile', '-of', action='store', metavar='fileName',
                help='path of the file where the output will be written')
        _ioPsSetup.set_defaults(func=self._setup)

        _ioPsRun = _ioPs.add_parser('run', help='run the model')
        _ioPsRun.add_argument('--layerNumbers', '-l', type=int, nargs='+',
                help='numbers of the layers whose information is requested; e.g. \"-n 3 8 9\"  means layers 3, 8, and 9; default includes all the layers')
        _ioPsRun.set_defaults(func=self._run)

        try:
            _args = _ioP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              
        except:             print("Unexpected error: {}".format(sys.exc_info()[0])); raise

        if len(vars(_args)) == 0:   pass                        # check for empty namespace 
        else:                       _args.func(_args)
