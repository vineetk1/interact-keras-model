'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
''''''
Commands to obtain static information about the model
'''
import logging
logger = logging.getLogger()
import classes.CommonModel as cm
import argparse
import shlex

class Model(cm.CommonModel):
    def __init__(self):
        pass

    def _modelInternal(self, _args):
        # print to stdout or a file the static information of the model
        _list = []
        if _args.summary:       _list.append(True); _list.append(cm.CommonModel.Kmodel.summary)
        if _args.configuration: _list.append(True); _list.append(cm.CommonModel.Kmodel.get_config)
        if _args.weights:       _list.append(True); _list.append(cm.CommonModel.Kmodel.get_weights)
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

        if _args.summary or _args.configuration or _args.weights:   self._modelInternal(_args)
        else:                                                       pass                           
        

