'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
'''
Commands specific to Natural Language Processing
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

class NLP(cm.CommonModel):
    def __init__(self):
        pass

    def _wordPatternsInWeights(self, _args):
        logger.debug('got here')

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
        _nlpP = argparse.ArgumentParser(prog="nlp", 
            description='Commands specific to Natural Language Processing',
            epilog='long options can be abbreviated if they are unambiguous in the commandline') 
        _nlpPs = _nlpP.add_subparsers()

        _nlpPsWp = _nlpPs.add_parser('wordPatternsInWeights', aliases=['wp'],
                help='find word-patterns in weights')
        _nlpPsWp.add_argument('--layerNumbers', '-l', type=int, nargs='+',
                help='numbers of the layers whose information is requested; e.g. \"-n 3 8 9\"  means layers 3, 8, and 9; default includes all the layers')
        _nlpPsWp.set_defaults(func=self._wordPatternsInWeights)

        try:
            _args = _nlpP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              
        except:             print("Unexpected error: {}".format(sys.exc_info()[0])); raise

        if len(vars(_args)) == 0:   pass                        # check for empty namespace 
        else:                       _args.func(_args)
