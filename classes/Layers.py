'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
'''
Commands to obtain static information about the layers of the model
'''
import logging
logger = logging.getLogger()
import classes.CommonModel as cm
import argparse
import shlex

class Layers(cm.CommonModel):
    def __init__(self):
        pass

    def _layersInfo(self, _args):
        # print to stdout or a file the static information about the layers of the model
        _list = []
        for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
            if (_args.layerNumbers is None) or (layerNum in _args.layerNumbers):
                _list.append(False); 
                _list.append('\nlayer {}: {}'.format(layerNum, layer.get_config()['name']))
                if _args.input:         
                    _list.append(False); _list.append(layer.input) 
                    _list.append(False); _list.append(layer.input_shape)
                if _args.output:        
                    _list.append(False); _list.append(layer.output) 
                    _list.append(False); _list.append(layer.output_shape)      
                if _args.configuration: _list.append(True); _list.append(layer.get_config)
                if _args.weights:       _list.append(True); _list.append(layer.get_weights)
        super().printStdoutOrFile(_args.outFile, _list)

    def settingsLoad(self, _settings):
        # upon start of this interactive program, load previously saved settings from _settings
        pass

    def settingsSave(self, _settings):
        # save the settings in _settings before exiting this interactive program
        pass

    def settingsDefault(self):
        # reset settings to their default state
        pass

    def settingsState(self):
        # print the settings at the stdout
        pass

    def execute(self, _line):
        # execute user input
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _layerP = argparse.ArgumentParser(prog="layers", 
            description='Get information on the layers',
            epilog='long options can be abbreviated if they are unambiguous in the commandline') 

        _layerP.add_argument('--numbers', '-n', metavar='layerNumbers', 
                dest='layerNumbers', type=int, nargs='+',
                help='''numbers of the layers whose information is requested; e.g. \"-n 3 8 9\"
                        means layers 3, 8, and 9; default includes all the layers''')
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
            _args = _layerP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              

        if _args.input or _args.output or _args.configuration or _args.weights: self._layersInfo(_args)
        else:                                                                   pass                           
