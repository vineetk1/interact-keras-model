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

class Layers(cm.CommonModel):
    def __init__(self):
        pass

    def _listNamesAndNumbers(self):
        logger.debug('got here')

    def _layersInfo(self, _args):
        if cm.CommonModel.Kmodel is None:
            print('No model file available. Must load a model file first')
            return
        if _args.outFile is None:
            for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
                if (_args.layerNumbers is None) or (layerNum in _args.layerNumbers):
                    print('\nlayer {}: {}'.format(layerNum, layer.get_config()['name']))
                    if _args.input:         print(layer.input); print(layer.input_shape)
                    if _args.output:        print(layer.output); print(layer.output_shape)
                    if _args.configuration: print(layer.get_config())
                    if _args.weights:       print(layer.get_weights())
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
                    for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
                        if (_args.layerNumbers is None) or (layerNum in _args.layerNumbers):
                            print('\nlayer {}: {}'.format(layerNum, layer.get_config()['name']))
                            if _args.input:         print(layer.input); print(layer.input_shape)
                            if _args.output:        print(layer.output); print(layer.output_shape)
                            if _args.configuration: print(layer.get_config())
                            if _args.weights:       print(layer.get_weights())

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
        _layerP = argparse.ArgumentParser(prog="layers", 
            description='Get information on the layers',
            epilog='long options can be abbreviated if they are unambiguous in the commandline') 

        _layerP.add_argument('--numbers', '-n', metavar='layerNumbers', 
                dest='layerNumbers', type=int, nargs='+',
                help='numbers of the layers whose information is requested; e.g. \"-n 3 8 9\"  means layers 3, 8, and 9; default includes all the layers')
        _layerP.add_argument('--input', '-i', action='store_true', 
                help='show the input tensors and shapes of the layers')
        _layerP.add_argument('--output', '-o', action='store_true', 
                help='show the output tensors and shapes of the layers')
        _layerP.add_argument('--configuration', '-c', action='store_true', 
                help='show the configuration of the layers')
        _layerP.add_argument('--weights', '-w', action='store_true', 
                help='show the weights of the layers')
        _layerP.add_argument('--outFile', '-f', action='store', metavar='fileName',
                help='path of the file where the output will be written')
        try:
            _args = _layerP.parse_args(shlex.split(_line))
            logger.debug('{}'.format(_args))
        except SystemExit: # normal exit
            return
        except:
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise   
        if _args.input or _args.output or _args.configuration or _args.weights: self._layersInfo(_args)
        else:                                                                   pass                           
