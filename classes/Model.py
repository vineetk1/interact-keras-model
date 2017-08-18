import logging
logger = logging.getLogger()
import pathlib
import h5py
import keras.models
import sys

class Model:
    def __init__(self):
        self._pathToModelFileName = ""

    def load(self, pathToModelFileName):
        try:
            self._pathToModelFileName = pathlib.Path(pathToModelFileName).expanduser().resolve()
        except FileNotFoundError:    
            print('file not found at {}'.format(pathToModelFileName))
            logger.debug('user filename convered to absolute path of {}'.format(self._pathToModelFileName))
            self._pathToModelFileName = ""
            return
        except:    
            print("unexpected error:", sys.exc_info()[0])
            logger.debug('user filename convered to absolute path of {}'.format(self._pathToModelFileName))
            raise   
        if not self._pathToModelFileName.is_file(): 
            print('file not found at {}'.format(self._pathToModelFileName))
            self._pathToModelFileName = ""
            return
        if not h5py.is_hdf5(self._pathToModelFileName):
            print('not a hdf5 file at {}'.format(self._pathToModelFileName))
            self._pathToModelFileName = ""
            return

    def summary(self):
        if not self._pathToModelFileName:
            print('no model file available')
            return
        #if not self._pathToModelFileName.is_file(): 
         #   print('path or file does not exist at {}'.format(self._pathToModelFileName))
          #  return
        try:
            kmodel = keras.models.load_model(self._pathToModelFileName)
        except FileNotFoundError:    
            print('file not found at {}'.format(self._pathToModelFileName))
            return
        except:    
            print("unexpected error:", sys.exc_info()[0])
            logger.debug('absolute path = {}'.format(self._pathToModelFileName))
            raise   
        kmodel.summary()
