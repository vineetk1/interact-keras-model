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
import contextlib 
#try:
    #import h5py
#except ImportError:
    #logger.info('h5py cannot be imported')    
    #h5py = None

class CommonModel:
    Kmodel = None

    def __init__(self):
        pass

    def absPathFile(self, _filePath):   # this method also used by subclasses
        # convenience method to reate an absolute path for the file _filepath
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

    def printStdoutOrFile(self, _outFile, _list):   # this method also used by subclasses
        # convenience method to print the contents of _list to the stdout or a file
        # _list has pairs -- _callable and _statement; if _statement is _callable then print(_statement()),
        # else print(_statement); print goes to stdout unless redirected to a file pointed to by _outFile
        if CommonModel.Kmodel is None:
            print('No model file available. Must load a model file first')
            return
        if _outFile is None:
            for _callable, _statement in zip(_list[::2], _list[1::2]):
                if _callable:   print(_statement())
                else:           print(_statement)
        else:
            try: _absOutFile = self.absPathFile(_outFile)   
            except: return
            with _absOutFile.open('w') as _outf:
                with contextlib.redirect_stdout(_outf):
                    for _callable, _statement in zip(_list[::2], _list[1::2]):
                        if _callable:   print(_statement())
                        else:           print(_statement)

    def _cmodelLoad(self, _inFile):
        # create a keras model from the file _inFile
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
        # upon start of this interactive program, load previously saved settings from _settings
        try: self._pathToModelFile = _settings['pathToModelFile']
        except:
            logger.warn('self._pathToModelFile not in settings = {}; settings file possibly corrupted'.format(
                _settings))
            raise
        # Following statement is not in a try-except block because exceptions are handled by the called method
        self._cmodelLoad(self._pathToModelFile)        # load Keras model

    def settingsSave(self, _settings):
        # save the settings in _settings before exiting this interactive program
        _settings['pathToModelFile'] = self._pathToModelFile

    def settingsDefault(self):
        # reset settings to their default state
        self._pathToModelFile = None
        CommonModel.Kmodel = None

    def settingsState(self):
        # print the settings at the stdout
        print('model file: {}'.format(self._pathToModelFile if self._pathToModelFile else None))

    def execute(self, _line):
        # execute user input
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
