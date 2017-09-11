'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
'''
Base class that has the model file and the model. Other classes inherit this information.
'''
import logging
logger = logging.getLogger()
import pathlib
import keras.models
import sys
import argparse
import shlex
#try:
    #import h5py
#except ImportError:
    #logger.info('h5py cannot be imported')    
    #h5py = None

class CommonModel:
    Kmodel = None

    def __init__(self):
        pass

    def absPathFile(self, _filePath):
        if _filePath is None:
            logger.debug('_filePath is None')
            raise 
        try:
            logger.debug('_filePath = {}'.format(_filePath))
            # Note: if _filePath="" then expanduser() expands it to current directory
            _absPathFile = pathlib.Path(_filePath).expanduser().resolve()
            logger.debug('_absPathFile = {}'.format(_absPathFile))
        except FileNotFoundError as err:   # Path does not exist    
            print('FileNotFoundError: {}'.format(err))
            raise
        except: print("Unexpected error: {}".format(sys.exc_info()[0])); raise
        if not _absPathFile.is_file():
            print('No file at {}'.format(_absPathFile))
            raise
        return _absPathFile

    def _cmodelLoad(self, _inFile):
        try: self._pathToModelFile = self.absPathFile(_inFile)
        except: 
            self._pathToModelFile = None
            CommonModel.Kmodel = None
            return
        try: CommonModel.Kmodel = keras.models.load_model(self._pathToModelFile)
        except ImportError as err:
            print('Import error: {}'.format(err))
            self._pathToModelFile = None
            CommonModel.Kmodel = None
            return
        except (ValueError, OSError) as err:
            print('Invalid {}\n{}'.format(self._pathToModelFile, err))
            self._pathToModelFile = None
            CommonModel.Kmodel = None
            return
        except:    
            self._pathToModelFile = None
            CommonModel.Kmodel = None
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise   

    def settingsLoad(self, _settings):
        try: self._pathToModelFile = _settings['pathToModelFile']
        except:
            logger.warn('self._pathToModelFile not in settings = {}; settings file possibly corrupted'.format(
                settigs))
            raise
        # Following statement is not in a try-except block because exceptions are handled by the called method
        self._cmodelLoad(self._pathToModelFile)        # load Keras model

    def settingsSave(self, _settings):
        _settings['pathToModelFile'] = self._pathToModelFile

    def settingsDefault(self):
        self._pathToModelFile = None
        CommonModel.Kmodel = None

    def settingsState(self):
        print('model file: {}'.format(self._pathToModelFile if self._pathToModelFile else None))

    def execute(self, _line):
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _commonModelP = argparse.ArgumentParser(prog="load", 
            description='Load the model',
            epilog='Long options can be abbreviated if they are unambiguous in the commandline') 
        _commonModelP.add_argument('inFile', action='store', metavar='inFile.h5',
                help='path of the file that has the model in HDF5 format')

        try:
            _args = _commonModelP.parse_args(shlex.split(_line))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              
        except:             print("Unexpected error: {}".format(sys.exc_info()[0])); raise

        if _args.inFile:    self._cmodelLoad(_args.inFile)
        else:               pass
