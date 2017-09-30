# Interact with Keras Model
This software is an interactive command-line program. It interacts with user-generated deep-learning keras-based models. The user does the following:
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
$> git clone https://github.com/vineetk1/interact-keras-model.git
```
The directory structure is as follows. The "interactKerasmodel.py" file has the main program.
```
$> cd interact-keras-model
$> ls
classes  interactKerasModel.py  LICENSE.txt  README.md
$> cd classes
$> ls
CommonModel.py  IO.py  Layers.py  Model.py  Session.py
```
## Usage
### Start the program
Run this interactive program from any directory. Note the message on "help". Enter commands following the prompt ">>" sign. 
```
$> python3 ~/interact-keras-model/interactKerasModel.py
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
Get help on any command. Help on the "session" command shows its usage, its description, and description of its arguments. 
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
Use "!" as an escape character to run shell commands from within this program.
```
>>!pwd
/home/vin/
>>
```
### Session
A session begins when a user starts this program and ends when the user exits the program. During the session, the user loads a model and specifies other settings. These settings are saved. Use "session -s" to examine the state of this session. The "model file" was loaded previously using the "load" command. The input file, "io input file", which has the input data, is also specified. The input data will be applied to the input layer number, "io input layer number", of 3. The output will be retrieved from the output layer number, "io output layer numbers", of 5. The output file, "io output file", is not loaded yet, so the output will be sent to the default standard-output (stdout). The "io expected output file" feature is not implemented, so it will not be described here.
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
Use the "load" command to load a keras model. Use "session -s" to display the session state.
```
>>load ~/deepLearningProject/deepLearningModel.h5
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 0
io output layer numbers: None
io input file: None
io expected output file: None
io output file: None
>>
```
### Model
Use the "model" command to display information about the model. This information includes the summary, configuration, and weights of the model. The output will be sent to the standard-output unless specified to be redirected to a file. Multiple dots in the last line show that the whole output is not shown in this example.
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
Use the "layers" command to display information about one or more layers of the model. This information includes the input tensor and shape, output tensor and shape, configuration, and weights. The output will be sent to the standard-output unless specified to be redirected to a file. Multiple dots in the last line show that the whole output is not shown in this example.
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
Use the 'io" command to display the outputs of specified layers when a specified input data is applied to an input of a specified layer. Use "io -h" to examine the details of the command. The "io" command has three sub-commands, namely, "listLayers", "setup", and "run"
```
>>io -h
usage: io [-h] {listLayers,ll,setup,se,run} ...

Commands specific to the Input and Output of the model

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
The "setup" sub-command sets up the model with arguments needed to later run the model. Use "io setup -h" to examine the details of this sub-command.
```
>>io se -h
usage: io setup [-h] [--inputLayerNumber INPUTLAYERNUMBER]
                [--outputLayerNumbers OUTPUTLAYERNUMBERS [OUTPUTLAYERNUMBERS ...]]
                [--exptdOutFile fileName] [--outFile fileName]
                inFile

positional arguments:
  inFile                path of an input file; the data will be read from this
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
                        path of an expected-output file; the data will be read
                        from this file and compared to an output from a layer
                        specified by "outputLayerNumbers"; the result of the
                        comparison will be written to a file specified by
                        "outFile" or to the default standard-output (stdout);
                        the file suffix must be ".npy" and it must be a numpy
                        array; ***Note: This feature is not implemented
  --outFile fileName, -of fileName
                        path of an output file; the output will be written to
                        this file
>>
```
Use "session -s" to examine the state of this session. The "model file" was loaded previously using the "load" command. The rest of the settings are default, and can be changed using the "setup" sub-command. The "io input file", which has the input data, is not loaded yet. The input data will be applied to the default "io input layer number" of 0. The "io output layer numbers" are not specified, so the default last layer number  will be picked when the model is run using the "run" sub-command. The "io output file" is not specifed yet, so the output will be sent to the standard-output (stdout). The "io expected output file" feature is not implemented.
```
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 0
io output layer numbers: None
io input file: None
io expected output file: None
io output file: None
>>
```
Specify the file that has the input data.
```
>>io setup ~/deepLearningProject/x_val.npy
>>
```
Use "session -s" to examine the state of this session. Note that "io output layer numbers" was not previously specified, so the "setup" sub-command automatically picked the default last layer number of the model. 
```
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 0
io output layer numbers: [10]
io input file: /home/vin/deepLearningProject/x_val.npy
io expected output file: None
io output file: None
>>
```
Run the model to display the output of the last layer. Multiple dots in the last line show that the whole output is not shown in this example.
```
>>io run
Processing may take a long time if the input data is large

layer 10: name = dense_2, shape = (5, 20), dtype = float32
[[  5.68623955e-06   3.49436968e-09   1.95091705e-13   9.26777457e-15
    1.39546920e-19   9.91854705e-08   4.45735493e-09   4.73716014e-17
    5.53826193e-16   2.03216000e-10   1.73403305e-06   2.11836313e-13
    6.45399478e-13   1.95926297e-09   5.40719379e-12   6.44911665e-07
    5.71678629e-06   1.65300360e-11   9.14643442e-06   9.99976873e-01]
 [  2.44325217e-22   4.42820536e-09   3.53693951e-19   1.68414225e-21
    9.35219544e-30   1.63039835e-20   3.36454784e-18   6.69618226e-33
    0.00000000e+00   7.42375461e-37   3.76892604e-30   9.38194314e-11
    1.19705479e-09   3.22347496e-11   1.00000000e+00   1.22737328e-22
    4.89322248e-18   2.14502930e-30   4.24237129e-14   2.37893777e-14]
......
>>
```
Change the settings to display the outputs of layers 6 and 8, and to redirect the outputs to the file "myFile".
```
>>io setup ~/deepLearningProject/x_val.npy -ol 6 8 -of myFile
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 0
io output layer numbers: [6, 8]
io input file: /home/vin/deepLearningProject/x_val.npy
io expected output file: None
io output file: /home/vin/interact-keras-model/myFile
>>
```
Run the model, and display the output from the file "myFile". Multiple dots show that the whole output is not shown in this example.
```
>>io run
Processing may take a long time if the input data is large
>>!cat myFile

layer 6: name = conv1d_3, shape = (5, 35, 128), dtype = float32
[[[ 0.          0.          0.07785349 ...,  0.          0.01855784  0.        ]
  [ 0.          0.          0.07785349 ...,  0.          0.01855784  0.        ]
  [ 0.          0.          0.07785349 ...,  0.          0.01855784  0.        ]
  ..., 
  [ 0.          0.          0.         ...,  0.          0.          0.        ]
  [ 0.          0.          0.         ...,  0.          0.          0.        ]
  [ 0.          0.          0.09836083 ...,  0.          0.09617352  0.        ]]
.......

layer 8: name = flatten_1, shape = (5, 128), dtype = float32
[[  4.36287403e-01   2.89763585e-02   6.91425800e-01   1.03442574e+00
    7.60179311e-02   0.00000000e+00   1.35375271e-02   4.51256752e-01
    0.00000000e+00   8.64261091e-01   0.00000000e+00   1.81727670e-02
    1.03881538e+00   0.00000000e+00   2.87368596e-01   0.00000000e+00
    0.00000000e+00   0.00000000e+00   7.26040900e-01   0.00000000e+00
......
>>
```
Change the settings to apply the input data to layer 2.
```
>>io setup ~/deepLearningProject/x_val.npy -ol 6 8 -of myFile -il 2
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 2
io output layer numbers: [6, 8]
io input file: /home/vin/deepLearningProject/x_val.npy
io expected output file: None
io output file: /home/vin/interact-keras-model/myFile
>>
```
Run the model. Note that the error message specifies the reason why the  model cannot be run.
```
>>io run
Processing may take a long time if the input data is large
Cannot feed value of shape (5, 1000) for Tensor 'embedding_1/Gather:0', which has shape '(?, 1000, 100)'
>>
```
### Quit, Exit, EOF
Use "quit" or "exit" or "eof" (i.e. cntrl-d) command to exit the session. Note the message that the session settings are automatically saved.
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
