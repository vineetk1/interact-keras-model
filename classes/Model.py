'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
import logging
logger = logging.getLogger()
import pathlib
import keras.models
import sys
import argparse
import shlex
from contextlib import redirect_stdout
#try:
    #import h5py
#except ImportError:
    #logger.info('h5py cannot be imported')    
    #h5py = None

class Model:
    def __init__(self):
        pass

    def _absPath(self, _filePath):
        if _filePath is None:
            logger.debug('_filePath is None')
            raise 
        try:
            logger.debug('_filePath = {}'.format(_filePath))
            # Note: if _filePath="" then expanduser() expands it to current directory
            _absPath = pathlib.Path(_filePath).expanduser().resolve()
            logger.debug('_absPath = {}'.format(_absPath))
        except FileNotFoundError as err:   # Path does not exist    
            print('FileNotFoundError: {}'.format(err))
            raise
        except:    
            print("Unexpected error:", sys.exc_info()[0])
            raise   
        return _absPath

    def _modelLoad(self, _inFile):
        try:
            logger.debug('_inFile = {}'.format(_inFile))
            _absInFile = self._absPath(_inFile)
            logger.debug('_absInFile = {}'.format(_absInFile))
        except:
            return
        try:
            self._kmodel = keras.models.load_model(_absInFile)
        except ImportError as err:
            print('Import error: {}'.format(err))
            return
        except ValueError as err:
            print('Value error: Invalid {}\n{}'.format(_absInFile, err))
            return
        except OSError as err:
            print('OS error: Invalid {}\n{}'.format(_absInFile, err))
            return
        except:    
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise   
        self._pathToModelFile = _absInFile

    def _kmodelPrint(self, _args):
        if self._pathToModelFile is None:
            print('No model file available. Must load a model file first')
            return
        if _args.outFile is None:
            if _args.summary:       self._kmodel.summary()
            if _args.configuration: print(self._kmodel.get_config())
            if _args.weights:       print(self._kmodel.get_weights())
        else:
            try:
                logger.debug('_args.outFile = {}'.format(_args.outFile))
                _absOutFile = self._absPath(_args.outFile)
                logger.debug('_absOutFile = {}'.format(_absOutFile))
            except:
                return
            if not _absOutFile.is_file():
                print('No file at {}'.format(_absOutFile))
                return
            with _absOutFile.open('w') as _outfile:
                with redirect_stdout(_outfile):
                    if _args.summary:       self._kmodel.summary()
                    if _args.configuration: print(self._kmodel.get_config())
                    if _args.weights:       print(self._kmodel.get_weights())

    def settingsLoad(self, _settings):
        if '_pathToModelFile' in _settings:
            self._pathToModelFile = _settings['_pathToModelFile']
            self._modelLoad(self._pathToModelFile)
        else:
            logger.warn('self._pathToModelFile not in settings = {}; settings file possibly corrupted'.format(
                settigs))
            raise

    def settingsSave(self, _settings):
        _settings['_pathToModelFile'] = self._pathToModelFile

    def settingsDefault(self):
        self._pathToModelFile = None

    def settingsState(self):
        print('model file: {}'.format(self._pathToModelFile if self._pathToModelFile else None))

    def _modelLd(self, _args):
        self._modelLoad(_args.inFile)

    def execute(self, _line):
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _modelP = argparse.ArgumentParser(prog="model", 
            description='Information on the model',
            epilog='Long options can be abbreviated if they are unambiguous in the commandline') 
        _modelPs = _modelP.add_subparsers()

        _modelPsLoad = _modelPs.add_parser('load', aliases=['lo'],
                help='load the model')
        _modelPsLoad.add_argument('inFile', action='store', metavar='fileName.h5',
                help='path of the file that has the model in HDF5 format')
        _modelPsLoad.set_defaults(func=self._modelLd)

        _modelPsPr = _modelPs.add_parser('print', aliases=['pr'],
                help='print the parameters of the model')
        _modelPsPr.add_argument('--summary', '-s', action='store_true', 
                help='show the configuration of the model')
        _modelPsPr.add_argument('--configuration', '-c', action='store_true', 
                help='show the configuration of the model')
        _modelPsPr.add_argument('--weights', '-w', action='store_true', 
                help='show the configuration of the model')
        _modelPsPr.add_argument('--outFile', '-f', action='store', metavar='fileName',
                help='path of the file where the output will be written')
        _modelPsPr.set_defaults(func=self._kmodelPrint)
        try:
            args = _modelP.parse_args(shlex.split(_line))
            logger.debug('{}'.format(args))
        except SystemExit: # normal exit
            return
        except:
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise   

        if len(vars(args)) == 0:        self.settingsState()    # check for empty namespace 
        else:                           args.func(args)
        

