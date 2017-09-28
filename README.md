# Interact with Keras Model
This software is an interactive command-line program. It interacts with user-generated deep learning keras based models. The user does the following:
1. Build a deep-learning model using Keras 
1. Interact with the model using this interactive command-line program
## Table of contents
<!-- vim-markdown-toc GFM -->
* [Requirements](#requirements)
* [Restrictions](#restrictions)
* [Installation](#installation)
* [Usage](#usage)
	* [Start the program](#start-the-program)
	* [Help](#help)
	* [Shell](#shell)
	* [Session](#session)
	* [Load](#load)
	* [Model](#model)
	* [Layers](#layers)
	* [IO (Input/Output)](#io-inputoutput)
	* [Quit, Exit, EOF](#quit-exit-eof)
* [Contribute to improve the software and add new features](#contribute-to-improve-the-software-and-add-new-features)
* [License](#license)

<!-- vim-markdown-toc -->
## Requirements
python >= 3.5, keras >= 2.0.2, numPy >= 1.12.1  
Lower versions may work. 
## Restrictions
* Currently works with Keras Sequential Model
* Software development and testing is done on Linux OS
## Installation
Clone this repository
```
git clone https://github.com/vineetk1/interact-keras-model.git
```
The directory structure is as follows. The "interactKerasmodel.py" file has the main program.
```
cd interact-keras-model
ls
classes  interactKerasModel.py  LICENSE.txt  README.md
cd classes
ls
CommonModel.py  IO.py  Layers.py  Model.py  Session.py
```
## Usage
### Start the program
Run the interactive program from any directory. Note the message on "help". Enter commands following the prompt ">>" sign. 
```
python3 ~/interact-keras-model/interactKerasModel.py
Using TensorFlow backend.
interactKerasModel version 0.7.0, Copyright (C) 2017, Interact with Keras based model. GPL-3.0+ open-source license.
Type "help" or "?" to list commands
>>
```
### Help
Type "help". A number of commands are listed.
```
>>help
Documented commands (type help <topic>):
========================================
EOF  exit  help  io  layers  load  model  quit  session  shell
>>
```
Get help on a command. Help on the "session" command shows its usage, its description, and description of its arguments. 
```
>>help session
usage: session [-h] [--default | --state]

Information and operations on the session

optional arguments:
  -h, --help     show this help message and exit
  --default, -d  clear the session with the default values
  --state, -s    show the state/status of the session

Long options can be abbreviated if they are unambiguous in the commandline
>>
```
Help can also be obtained using "-h". Multiple dots in the last line show that the whole output is not shown in this example.
```
>>session -h
usage: session [-h] [--default | --state]
.....
```
### Shell
Use "!" as escape character to run shell commands from within this program.
```
>>!pwd
/home/vin/
>>
```
### Session
A session begins when a user starts the program and ends when the user exits the program. During the session, the user loads a model and specifies other settings. These settings are saved. Use "session -s" to examine the state of this session. The "model file" was loaded previously using the "load" command. The "io input file", which provides the input data, is also specified. The input data will be applied to the "io input layer number" of 3. The output will be retrieved from the "io output layer numbers" of 5. The "io output file" is not loaded yet, so the output will be sent to the default standard-output (stdout). The "io expected output file" is not implemented yet, so it will not be described here.
```
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 3
io output layer numbers: [5]
io input file: /home/vin/interact-keras-model/x_val_file.npy
io expected output file: /home/vin/interact-keras-model/y_val_file.npy
io output file: None
>>
```
The state of the session is saved forever, unless it is changed or reset to its default values through the "session -d" command.
```
>>session -d
>>session -s
model file: None
io input layer number: 0
io output layer numbers: None
io input file: None
io expected output file: None
io output file: None
>>
```
For help on the session command, use "session -h" 
### Load
Use the "load" command to load a keras model.
```
>>load ~/deepLearningProject/deepLearningModel.h5
>>
```
### Model
Use the "model" command to display information about the model. This information includes the summary, configuration, and weights of the model. The output will be sent to the standard-output, unless specified to be redirected to a file. Multiple dots in the last line show that the whole output is not shown in this example.
```
>>!touch myFile
>>model -s -c -w -of myFile
>>!more myFile
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         (None, 1000)              0         
_________________________________________________________________
embedding_1 (Embedding)      (None, 1000, 100)         2000100   
_________________________________________________________________
conv1d_1 (Conv1D)            (None, 996, 128)          64128     
_________________________________________________________________
.....
>>
```
### Layers
The "layers" command displays information about one or more layers in the model. This information includes the input tensor and shape, output tensor and shape, configuration, and weights. The output will be sent to the standard-output, unless specified to be redirected to a file. Multiple dots in the last line show that the whole output is not shown in this example.
``` 
>>layers -l 2 10 -i -o -c -w

layer 2: name = conv1d_1, Input Tensor and Shape
Tensor("embedding_1_3/Gather:0", shape=(?, 1000, 100), dtype=float32)
(None, 1000, 100)

layer 2: name = conv1d_1, Output Tensor and Shape
Tensor("conv1d_1_3/Relu:0", shape=(?, 996, 128), dtype=float32)
(None, 996, 128)

layer 2: name = conv1d_1, Configuration
{'activation': 'relu', 'name': 'conv1d_1', 'bias_constraint': None, 'kernel_regularizer': None, 'activity_regularizer': None, 'bias_initializer':
.....
>>
```
### IO (Input/Output)
The 'io" command displays the outputs from the specified layers when a specified input data is applied to a layer. Use "io -h" to examine the details of the command. The "io" command has three sub-commands, namely, "listLayers", "setup", and "run"
```
>>io -h
usage: io [-h] {listLayers,ll,setup,se,run} ...

Commands specific to Input and Output of the model

positional arguments:
  {listLayers,ll,setup,se,run}
    listLayers (ll)     list the numbers and names of all the layers
    setup (se)          setup the model before running it
    run                 run the model

optional arguments:
  -h, --help            show this help message and exit

long options can be abbreviated if they are unambiguous in the commandline
>>
```
The "listLayers" sub-command displays the names and numbers of all the layers in the model.
```
>>io ll
layer 0: input_1          layer 1: embedding_1      layer 2: conv1d_1         layer 3: max_pooling1d_1  layer 4: conv1d_2         layer 5: max_pooling1d_2  layer 6: conv1d_3         layer 7: max_pooling1d_3  layer 8: flatten_1        layer 9: dense_1          layer 10: dense_2          
>>
```
The "setup" sub-command sets up the model with arguments needed to run the model. Use "io setup -h" to examine the details of the sub-command.
```
>>io se -h
usage: io setup [-h] [--inputLayerNumber INPUTLAYERNUMBER]
                [--outputLayerNumbers OUTPUTLAYERNUMBERS [OUTPUTLAYERNUMBERS ...]]
                [--exptdOutFile fileName] [--outFile fileName]
                inFile

positional arguments:
  inFile                path of a input file; the data will be read from this
                        file and applied to the input of a layer specified by
                        "inputLayerNumber"; the file suffix must be ".npy" and
                        it must be a numpy array

optional arguments:
  -h, --help            show this help message and exit
  --inputLayerNumber INPUTLAYERNUMBER, -il INPUTLAYERNUMBER
                        input data will be applied to this specified layer
                        number; e.g. "-il 5" means that the input will be
                        applied to layer 5; the default is the first layer,
                        i.e. layer 0
  --outputLayerNumbers OUTPUTLAYERNUMBERS [OUTPUTLAYERNUMBERS ...], -ol OUTPUTLAYERNUMBERS [OUTPUTLAYERNUMBERS ...]
                        outputs will be retrieved from the specified layer
                        numbers; e.g. "-ol 3 8 9" means that the outputs will
                        be retrieved from layers 3, 8, and 9; the default is
                        the last layer
  --exptdOutFile fileName, -ef fileName
                        path of a expected-output file; the data will be read
                        from this file and compared to an output from a layer
                        specified by "outputLayerNumbers"; the result of the
                        comparison will be written to a file specified by
                        "outFile" or to the default standard-output (stdout);
                        the file suffix must be ".npy" and it must be a numpy
                        array; ***Note: This feature is not implemented yet
  --outFile fileName, -of fileName
                        path of an output file; the output will be written to
                        this file
>>
```
Use "session -s" to examine the state of this session. The "model file" was loaded previously using the "load" command. The rest of the settings are default. The "io input file", which provides the input data, is not loaded yet. The input data will be applied to the "io input layer number" of 0. The output will be retrieved from the last layer of the model, which in this case is the "io output layer numbers" of 10. The "io output file" is not loaded yet, so the output will be sent to the standard-output (stdout).   
```
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 0
io output layer numbers: [10]
io input file: None
io expected output file: None
io output file: None
>>
```


### Quit, Exit, EOF
Use "quit" or "exit" or "eof" (i.e. cntrl-d) command to exit the session. Note that the session settings are automatically saved.
```
>>quit
Session settings saved
```
## Contribute to improve the software and add new features
Open an Issue as follows:
1. Go to the repository page on github. Click on the "Issues" button in the repo header.
1. Click on the "New Issue" button.
1. Provide sufficient information so a decision, regarding the issue, can be made promptly.
1. Click on the "Submit new issue" button.   

If the decision is positive, follow these steps to improve/add to the software:
1. Fork this repository.
1. Create a new branch (git checkout -b newBranch).
1. Make the appropriate changes in the files, and add new files.
1. Add files (git add fileName1.py fileName2.py ....).
1. Commit changes (git commit -m 'synopsis of the changes').
1. Push to the branch (git push origin newBranch).
1. Go to the repository page on github. Click on the "Pull Requests" button in the repo header, and follow directions.
## License
This software is available for free under the terms of the GPL-3.0+ Open Source license. 
