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
	* [Getting started](#getting-started)
	* [Help](#help)
* [Contribute to improve the software and add new features](#contribute-to-improve-the-software-and-add-new-features)
* [License](#license)

<!-- vim-markdown-toc -->
## Requirements
python >= 3.5, keras >= 2.0.2, numPy >= 1.12.1  
Lower versions may work. Try at your own risk!
## Restrictions
* Currently works with Keras Sequential Model
* Software development and testing is done on Linux OS
## Installation
Clone this repository
```
git clone https://github.com/vineetk1/interact-keras-model.git
```
## Usage
### Getting started
Run the program
```
#Provide the path to the interact-keras-model directory
python3 ~/interact-keras-model/interactKerasModel.py
Using TensorFlow backend.
interactKerasModel version 0.7.0, Copyright (C) 2017, Interact with Keras based model. GPL-3.0+ open-source license.
Type "help" or "?" to list commands

>>help
Documented commands (type help <topic>):
========================================
EOF  exit  help  model  quit  session  shell

>>
```
Enter commands following the prompt ">>" sign.
### Help

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
