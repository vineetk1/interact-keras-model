'''
Vineet Kumar, Copyright (C) 2017, GPL-3.0+ open-source license.
This program comes with ABSOLUTELY NO WARRANTY.
'''
'''
Commands to obtain the outputs of the various layers in the model, for a given input
'''
import logging
logger = logging.getLogger()
import classes.CommonModel as cm
#import keras.models
import sys
import argparse
import shlex
import keras.backend
import numpy

class IO(cm.CommonModel):
    def __init__(self):
        pass

    def _listLayersNumbersNames(self, _args):
        # output to stdout a list of layer numbers and names of the model
        for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
            print('layer {}: {:17}'.format(layerNum, layer.get_config()['name']), end="")
        print('\n')

    def numpyLoadFile(self, _file):
        # convenience method to deserializes a numpy file _file
        try: deserializedFile = numpy.load(_file)
        except (ValueError, OSError) as err:
            print('Invalid {}\n{}'.format(_file, err))
            raise
        except: print("Unexpected error: {}".format(sys.exc_info()[0])); raise
        return deserializedFile

    def _setup(self, _args):
        # setup the parameters to enable the model to be run
        self._inputLayerNumber = _args.inputLayerNumber
        self._outputLayerNumbers = _args.outputLayerNumbers
        if self._outputLayerNumbers is None:
            # get the number of the last layer; is there a better way of getting this number?
            for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
                outputLastLayerNum = layerNum
            self._outputLayerNumbers = [outputLastLayerNum] 
        try: 
            self._inFile = super().absPathFile(_args.inFile)
            self._input = self.numpyLoadFile(self._inFile)
            print('input file: type = {}, shape = {}, dtype = {}'.format(
                        type(self._input), self._input.shape, self._input.dtype))
        except: 
            self._inFile = None
            self._input = None
        try: 
            self._exptdOutFile = super().absPathFile(_args.exptdOutFile)
            self._exptdOutput = self.numpyLoadFile(self._exptdOutFile)
            print('expected output file: type = {}, shape = {}, dtype = {}\n{}'.format(
                        type(self._exptdOutput), self._exptdOutput.shape, 
                        self._exptdOutput.dtype, self._exptdOutput[0:1]))
        except: 
            self._exptdOutFile = None
            self._exptdOutput = None
        try: self._outFile = super().absPathFile(_args.outFile)
        except: self._outFile = None

    def _run(self, _args):
        # run the model to produce outputs for a given input
        if cm.CommonModel.Kmodel is None:
            print('No model file available. Must load a model file first')
            return
        if self._input is None:
            print('No input file available. Must specify an input file first')
            return
        if self._outFile is None:
            for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
                if layerNum in _args.outputLayerNumbers:
                    referenceToClass_tensorflowBackendFunction = keras.backend.function([cm.CommonModel.Kmodel.layers[0].input], [cm.CommonModel.Kmodel.layers[layerNum].output])
                    layerOutput = referenceToClass_tensorflowBackendFunction([self._input[0:1]])[0]
                    print('\nlayer {}: name = {}, type = {}, shape = {}, dtype = {}\n{}'.format(
                        layerNum, layer.get_config()['name'], type(layerOutput), layerOutput.shape, 
                        layerOutput.dtype, layerOutput))

    def settingsLoad(self, _settings):
        # upon start of this interactive program, load previously saved settings in _settings
        try:
            self._inputLayerNumber = _settings['ioInputLayerNumber']
            self._outputLayerNumbers = _settings['ioOutputLayerNumbers']
            self._inFile = _settings['ioInFile']
            self._exptdOutFile = _settings['ioExptdOutFile']
            self._outFile = _settings['ioOutFile']
        except:
            logger.warn('one or more IO files  not in settings = {}; settings file possibly corrupted'.format(
                _settings))
            raise

    def settingsSave(self, _settings):
        # save the settings in _settings before exiting this interactive program
        _settings['ioInputLayerNumber'] = self._inputLayerNumber
        _settings['ioOutputLayerNumbers'] = self._outputLayerNumbers
        _settings['ioInFile'] = self._inFile
        _settings['ioExptdOutFile'] = self._exptdOutFile
        _settings['ioOutFile'] = self._outFile

    def settingsDefault(self):
        # reset settings to their default state
        self._inputLayerNumber = None
        self._outputLayerNumbers = None
        self._inFile = None
        self._exptdOutFile = None
        self._outFile = None

    def settingsState(self):
        # print the settings at the stdout
        print('io input layer number: {}'.format(self._inputLayerNumber))
        print('io output layer numbers: {}'.format(self._outputLayerNumbers))
        print('io input file: {}'.format(self._inFile if self._inFile else None))
        print('io expected output file: {}'.format(self._exptdOutFile if self._exptdOutFile else None))
        print('io output file: {}'.format(self._outFile if self._outFile else None))

    def execute(self, _line):
        # execute user input
        logger.debug('_line = {}, shlex.split(_line) = {}'.format(_line, shlex.split(_line)))
        _ioP = argparse.ArgumentParser(prog="io", 
            description='Commands specific to Input and Output of the model',
            epilog='long options can be abbreviated if they are unambiguous in the commandline') 
        _ioPs = _ioP.add_subparsers()

        _ioPsListLayers = _ioPs.add_parser('listLayers', aliases=['ll'],
                help='list the numbers and names of all the layers')
        _ioPsListLayers.set_defaults(func=self._listLayersNumbersNames)

        _ioPsSetup = _ioPs.add_parser('setup', aliases=['se'],
                help='setup the model before running it')
        #_ioPsSetup.add_argument('--inFile', '-if', action='store', metavar='fileName',
        #_ioPsSetup.add_argument('inFile', action='store', metavar='fileName',
        _ioPsSetup.add_argument('inFile', action='store', 
                help='path of the file that has the input to the model; the file must be a numpy array')
        _ioPsSetup.add_argument('--inputLayerNumber', '-il', type=int, action='store', default = 0,
                help='input will be applied to the specified layer number; e.g. \"-il 5\" means that the input will be applied to layer 5; default includes the first layer, i.e. layer 0')
        _ioPsSetup.add_argument('--outputLayerNumbers', '-ol', type=int, nargs='+',
                help='outputs will be retrieved from the specified layer numbers; e.g. \"-ol 3 8 9\" means that the outputs will be retrieved from layers 3, 8, and 9; default includes only the last layer')
        _ioPsSetup.add_argument('--exptdOutFile', '-ef', action='store', metavar='fileName',
                help='path of the file that has the expected output of the last layer only; the file must be a numpy array')
        _ioPsSetup.add_argument('--outFile', '-of', action='store', metavar='fileName',
                help='path of the file where the output will be written')
        _ioPsSetup.set_defaults(func=self._setup)

        _ioPsRun = _ioPs.add_parser('run', help='run the model')
        _ioPsRun.set_defaults(func=self._run)

        try:
            _args = _ioP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              
        except:             print("Unexpected error: {}".format(sys.exc_info()[0])); raise

        if len(vars(_args)) == 0:   pass                        # check for empty namespace 
        else:                       _args.func(_args)
