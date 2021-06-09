# At session start

Connexion to sma6255 station via

	ssh sma6255

Start shell zsh via

	zsh

Go to unitest folder via

	cd /C/autools/source/$(whoami)/unitest

Modify the environment variable $PATH via

	source export_path

# SCADE generation 

Verify SCADE specific configuration « unitest ».
Untick the option « Use CopyMem », avalaible in Project->Code Generator->Setting, tab Configuration

Generate node via SCADE

Copy manually the SCADE generated sources into the folder /kcg/<NODE_NAME> with Windows

# For each new node version

Suppress the SCADE includes in the file unitest/kcg/<NODE_NAME>/scade_type.h

Installation of the new instance via

	unitest_prepare <NODE_NAME>

Remark : the unitest environment is located in the folder build/<NODE_NAME>

# How to start a simulation

Create a test folder in build/<NODE_NAME>/replay

	mkdir testXX

From the folder build/<NODE_NAME>/replay/testXX, copy the file inputs.tsv (scenario) in the folder and modify it, (variable modification / addition of lines)

Start the scenario for the node

	unitest_replay <NODE_NAME> <testXX>

The outputs are available in the file testXX/output.tsv
