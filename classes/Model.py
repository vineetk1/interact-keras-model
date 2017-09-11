'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
''''''
Commands to obtain static information about the model
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
#try:
    #import h5py
#except ImportError:
    #logger.info('h5py cannot be imported')    
    #h5py = None

class Model(cm.CommonModel):
    def __init__(self):
        pass

    def _modelInternal(self, _args):
        if cm.CommonModel.Kmodel is None:
            print('No model file available. Must load a model file first')
            return
        if _args.outFile is None:
            if _args.summary:       cm.CommonModel.Kmodel.summary()
            if _args.configuration: print(cm.CommonModel.Kmodel.get_config())
            if _args.weights:       print(cm.CommonModel.Kmodel.get_weights())
        else:
            try:    _absOutFile = super().absPathFile(_args.outFile)
            except: return
            with _absOutFile.open('w') as _outfile:
                with contextlib.redirect_stdout(_outfile):
                    if _args.summary:       cm.CommonModel.Kmodel.summary()
                    if _args.configuration: print(cm.CommonModel.Kmodel.get_config())
                    if _args.weights:       print(cm.CommonModel.Kmodel.get_weights())

    def settingsLoad(self, _settings):
        pass

    def settingsSave(self, _settings):
        pass

    def settingsDefault(self):
        pass

    def settingsState(self):
        pass

    def execute(self, _line):
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _modelP = argparse.ArgumentParser(prog="model", 
            description='Get information on the model',
            epilog='long options can be abbreviated if they are unambiguous in the commandline') 
        _modelP.add_argument('--summary', '-s', action='store_true', 
                help='show the summary of the model')
        _modelP.add_argument('--configuration', '-c', action='store_true', 
                help='show the configuration of the model')
        _modelP.add_argument('--weights', '-w', action='store_true', 
                help='show the weights of the model')
        _modelP.add_argument('--outFile', '-f', action='store', metavar='fileName',
                help='path of the file where the output will be written')

        try:
            _args = _modelP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              
        except:             print("Unexpected error: {}".format(sys.exc_info()[0])); raise

        if _args.summary or _args.configuration or _args.weights:   self._modelInternal(_args)
        else:                                                       pass                           
        

