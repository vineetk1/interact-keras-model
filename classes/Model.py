'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
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
            try:
                logger.debug('_args.outFile = {}'.format(_args.outFile))
                _absOutFile = super().absPath(_args.outFile)
                logger.debug('_absOutFile = {}'.format(_absOutFile))
            except:
                return
            if not _absOutFile.is_file():
                print('No file at {}'.format(_absOutFile))
                return
            with _absOutFile.open('w') as _outfile:
                with contextlib.redirect_stdout(_outfile):
                    if _args.summary:       cm.CommonModel.Kmodel.summary()
                    if _args.configuration: print(cm.CommonModel.Kmodel.get_config())
                    if _args.weights:       print(cm.CommonModel.Kmodel.get_weights())

    def settingsload(self, _settings):
        pass

    def settingssave(self, _settings):
        pass

    def settingsdefault(self):
        pass

    def settingsstate(self):
        pass

    def execute(self, _line):
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _modelP = argparse.ArgumentParser(prog="model", 
            description='information on the model',
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
            _args = _modelP.parse_args(shlex.split(_line))
            logger.debug('{}'.format(_args))
        except SystemExit: # normal exit
            return
        except:
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise   
        if len(vars(_args)) == 0:       pass                    # check for empty namespace 
        else:                           self._modelInternal(_args)
        

