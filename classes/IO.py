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
import argparse
import shlex
import keras.backend
import numpy

class IO(cm.CommonModel):
    def __init__(self):
        pass

    def _listLayersNumbersNames(self, _args):
        # output to stdout a list of layer numbers and names of the model
        for _layerNum, _layer in enumerate(cm.CommonModel.Kmodel.layers): 
            print('layer {}: {:17}'.format(_layerNum, _layer.get_config()['name']), end="")
        print('\n')

    def _lastLayerNum(self):
        # convenience method to get the layer number of the last layer in the model
        try:
            # is there a better method of getting the number of the last layer?
            for _layerNum, _layer in enumerate(cm.CommonModel.Kmodel.layers): pass
            return _layerNum
        except: return None # cm.CommonModel.Kmodel is None

    def _numpyLoadFile(self, _file):
        # convenience method to deserializes a numpy file _file
        try: _deserializedFile = numpy.load(_file)
        except (ValueError, OSError) as error:
            logger.debug('{}: {}'.format(type(error).__name__, error))
            print('Invalid {}; {}'.format(_file, error)); raise
        return _deserializedFile

    def _setup(self, _args):
        # setup the parameters to enable the model to run
        self._inputLayerNumber = _args.inputLayerNumber
        assert(self._inputLayerNumber is not None) # if assert fails, it will crash the program
        self._outputLayerNumbers = _args.outputLayerNumbers
        if self._outputLayerNumbers is None:
            _lastLayerNum = self._lastLayerNum()
            if _lastLayerNum is not None: self._outputLayerNumbers = [_lastLayerNum]
        try: 
            self._inFile = super().absPathFile(_args.inFile)
            self._inputData = self._numpyLoadFile(self._inFile)
        except (FileNotFoundError, ValueError, OSError): self._inFile = None; self._inputData = None
        try: 
            self._exptdOutFile = super().absPathFile(_args.exptdOutFile)
            self._exptdOutput = self._numpyLoadFile(self._exptdOutFile)
        except (FileNotFoundError, ValueError, OSError): self._exptdOutFile = None; self._exptdOutput = None
        else: 
            print('The feature of comparing the model output with the expected-output is not ', end="")
            print('implemented yet')
        try: self._outFile = super().absPathFile(_args.outFile)
        except FileNotFoundError: self._outFile = None

    def _run(self, _args):
        # run the model to produce outputs for a given input
        if cm.CommonModel.Kmodel is None:
            print('No model file available. Must load a model file first. Cannot force run using \"run -f\"')
            return
        if self._inputData is None:
            print('No input file available. Must load an input file first. Cannot force run using \"run -f\"')
        assert(self._inputLayerNumber is not None)
        _lastLayerNum = self._lastLayerNum()
        if (self._inputLayerNumber < 0) or (self._inputLayerNumber > _lastLayerNum):
            print("Input layer {} does not exist. Using default layer 0 instead".format(
                self._inputLayerNumber))
            self._inputLayerNumber = 0
        if self._outputLayerNumbers is None:
            self._outputLayerNumbers = [_lastLayerNum]
            print("No ouput layer specified. Using default last layer {}".format(self._outputLayerNumbers))

        shouldReturn = False
        if self._inputData.shape[1] != cm.CommonModel.Kmodel.layers[self._inputLayerNumber].input_shape[1]:
                print('Shape {} of data in input-file MUST be equal to shape {} of input in layer {}'.format(
                self._inputData.shape,  cm.CommonModel.Kmodel.layers[self._inputLayerNumber].input_shape, 
                self._inputLayerNumber))
                shouldReturn = True
        if (self._exptdOutput is not None):
            print('The feature of comparing the model output with the expected-output is not implemented yet')
        #if (self._exptdOutput is not None) and (len(self._outputLayerNumbers) != 1):
        #   print('The expected-output-file MUST be associated with only one output-layer {}'.format(
        #      self._outputLayerNumbers))
        #    shouldReturn = True
        if shouldReturn and (not _args.force): return

        for layerNum, layer in enumerate(cm.CommonModel.Kmodel.layers): 
            if layerNum in self._outputLayerNumbers:
                referenceToClass_tensorflowBackendFunction = keras.backend.function(
                        [cm.CommonModel.Kmodel.layers[self._inputLayerNumber].input], [layer.output])
                layerOutput = referenceToClass_tensorflowBackendFunction([self._inputData[0:1]])[0]
                print('\nlayer {}: name = {}, type = {}, shape = {}, dtype = {}\n{}'.format(
                        layerNum, layer.get_config()['name'], type(layerOutput), layerOutput.shape, 
                        layerOutput.dtype, layerOutput))


    def settingsLoad(self, _settings):
        # upon start of this interactive program, load previously saved settings from _settings
        try:
            _inputLayerNumber = _settings['ioInputLayerNumber']
            _outputLayerNumbers = _settings['ioOutputLayerNumbers']
            _inFile = _settings['ioInFile']
            _exptdOutFile = _settings['ioExptdOutFile']
            _outFile = _settings['ioOutFile']
        except KeyError: raise
        _args = argparse.Namespace(inputLayerNumber=locals()["_inputLayerNumber"], 
                outputLayerNumbers=locals()["_outputLayerNumbers"], inFile=locals()["_inFile"], 
                exptdOutFile=locals()["_exptdOutFile"], outFile=locals()["_outFile"])
        logger.debug(_args)
        # Following statement is not in a try-except block because exceptions are handled by the 
        # called method
        self._setup(_args)

    def settingsSave(self, _settings):
        # save the settings in _settings before exiting this interactive program
        _settings['ioInputLayerNumber'] = self._inputLayerNumber
        _settings['ioOutputLayerNumbers'] = self._outputLayerNumbers
        _settings['ioInFile'] = self._inFile
        _settings['ioExptdOutFile'] = self._exptdOutFile
        _settings['ioOutFile'] = self._outFile

    def settingsDefault(self):
        # reset settings to their default state
        self._inputLayerNumber = 0 
        self._outputLayerNumbers = None         # None because cm.CommonModel.Kmodel is None
        self._inFile = None
        self._exptdOutFile = None
        self._outFile = None

    def settingsState(self):
        # print the settings at the stdout
        print('io input layer number: {}'.format(self._inputLayerNumber))
        print('io output layer numbers: {}'.format(self._outputLayerNumbers))
        print('io input file: {}'.format(self._inFile))
        print('io expected output file: {}'.format(self._exptdOutFile))
        print('io output file: {}'.format(self._outFile))

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
        _ioPsSetup.add_argument('inFile', action='store', 
                help='''path of a input file; the data will be read from this file and applied
                        to the input of a layer specified by "inputLayerNumber";
                        the file suffix must be ".npy" and it  must be a numpy array''')
        _ioPsSetup.add_argument('--inputLayerNumber', '-il', type=int, action='store', default = 0,
                help='''input data will be applied to this specified layer number; e.g. \"-il 5\"
                        means that the input will be applied to layer 5; the default is the 
                        first layer, i.e. layer 0''')
        _ioPsSetup.add_argument('--outputLayerNumbers', '-ol', type=int, nargs='+',
                help='''outputs will be retrieved from the specified layer numbers; e.g. \"-ol 3 8 9\" 
                        means that the outputs will be retrieved from layers 3, 8, and 9; the  
                        default is the last layer''')
        _ioPsSetup.add_argument('--exptdOutFile', '-ef', action='store', metavar='fileName',
                help='''path of a expected-output file; the data will be read from this file
                        and compared to an output from a layer specified by "outputLayerNumbers";
                        the result of the comparison will be written to a file specified by 
                        "outFile" or to the default standard-output (stdout); the file
                        suffix must be ".npy" and it  must be a numpy array; ***Note: This feature
                        is not implemented yet''')
        _ioPsSetup.add_argument('--outFile', '-of', action='store', metavar='fileName',
                help='path of an output file; the output will be written to this file')
        _ioPsSetup.set_defaults(func=self._setup)

        _ioPsRun = _ioPs.add_parser('run', help='run the model')
        _ioPsRun.add_argument('--force', '-f', action='store_true', 
                help='force the model to run even when errors are flagged')
        _ioPsRun.set_defaults(func=self._run)

        try:
            _args = _ioP.parse_args(shlex.split(_line if _line else '-h'))
            logger.debug('{}'.format(_args))
        except SystemExit:  return                              

        #if len(vars(_args)) == 0:   pass                        # check for empty namespace 
        _args.func(_args)
