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
	* [Session](#session)
	* [Load](#load)
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
### Session
A session begins when a user starts the program and ends when the user exits the program. During the session, the user loads a model and specifies other settings. These settings are saved, and this state can be displayed through the "session -s" command.
```
>>session -s
model file: /home/vin/deepLearningProject/deepLearningModel.h5
io input layer number: 3
io output layer numbers: [5]
io input file: /home/vin/interact-keras-model/x_val_file.npy
io expected output file: /home/vin/interact-keras-model/y_val_file.npy
io output file: None
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
The details of the session command can be displayed using "session -h" 
### Load




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
