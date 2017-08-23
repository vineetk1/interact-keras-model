import logging
logger = logging.getLogger()
import pathlib
import h5py
import keras.models
import sys
import argparse
import shlex

class Model:
    def __init__(self):
        self._pathToModelFile = ""

    def _modelFile(self, pathToModelFile):
        try:
            self._pathToModelFile = pathlib.Path(pathToModelFile).expanduser().resolve()
        except FileNotFoundError:    
            print('File not found at {}'.format(pathToModelFile))
            logger.debug('user filename convered to absolute path of={}'.format(self._pathToModelFile))
            self._pathToModelFile = ""
            return
        except:    
            print("Unexpected error:", sys.exc_info()[0])
            logger.debug('user filename convered to absolute path of={}'.format(self._pathToModelFile))
            raise   
        if not h5py.is_hdf5(self._pathToModelFile):
            print('Not a hdf5 file at {}'.format(self._pathToModelFile))
            self._pathToModelFile = ""
            return

    def _summary(self):
        if not self._pathToModelFile:
            print('No model file available')
            return
        try:
            kmodel = keras.models.load_model(self._pathToModelFile)
        except FileNotFoundError:    
            print('File not found at {}'.format(self._pathToModelFile))
            return
        except:    
            print("Unexpected error:", sys.exc_info()[0])
            logger.debug('absolute path={}'.format(self._pathToModelFile))
            raise   
        kmodel.summary()

    def load(self, settings):
        if '_pathToModelFile' in settings:
            self._pathToModelFile = settings['_pathToModelFile']
        else:
            logger.warn('self._pathToModelFile not in settings={}; settings file possibly corrupted'.format(
                settigs))
            raise

    def save(self, settings):
        settings['_pathToModelFile'] = self._pathToModelFile

    def default(self):
        self._pathToModelFile = ""

    def state(self):
        print('model file: {}'.format(self._pathToModelFile if self._pathToModelFile else None))

    def execute(self, line):
        logger.debug('line={}, shlex.split(line)={}'.format(line, shlex.split(line)))
        self._modelP = argparse.ArgumentParser(prog="model", 
            description='Information on the model',
            epilog='Long options can be abbreviated if they are unambiguous in the commandline') 
        self._modelP.add_argument('--file', '-f', action='store', metavar='fileName.h5',
                help='path to the file that has the model in HDF5 format')
        self._modelP.add_argument('--summary', '-s', action='store_true', 
                help='show the summary of the model')
        try:
            args = self._modelP.parse_args(shlex.split(line))
            logger.debug('{}'.format(args))
        except SystemExit:
            return
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise   
        if args.file:                           self._modelFile(args.file)
        if args.summary:                        self._summary()
        if not (args.file or args.summary):    self.state()   
