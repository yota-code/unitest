# First use of unitest

Verify your .zshrc and .profile after connexion to sma6255

	ssh sma6255
	zsh
	cd
	ls -la .profile
	ls -la .zshrc

Results should be .profile -> /C/autools/zprofile/profile and .zshrc -> /C/autools/zprofile/zshrc
if not, create the following links:

	ln -snf /C/autools/zprofile/profile .profile 
	ln -snf /C/autools/zprofile/.zshrc .zshrc 

Create if needed your personal folder on \\nahar\fdat1038\source\ with aXXXXX (or echo $(whoami))

Install unitest in your folder on \\nahar\fdat1038\source\aXXXX via git clone
URL http://sma6299.eu.eurocopter.corp/gitea/ETGGC/unitest

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

Copy manually the SCADE generated sources into the folder /kcg/<NODE_NAME> with Windows (create it if needed)

# For each new node version

Suppress the SCADE includes in the file unitest/kcg/<NODE_NAME>/scade_type.h

Installation of the new instance via

	unitest_prepare <NODE_NAME> <template_name>

With as template helionix / scade_v3 / scade_mini

Remark : the unitest environment is located in the folder build/<NODE_NAME>

# How to start a simulation

Create a test folder in build/<NODE_NAME>/replay

	mkdir testXX

From the folder build/<NODE_NAME>/replay/testXX, copy the file inputs.tsv (scenario) in the folder and modify it, (variable modification / addition of lines)

Start the scenario for the node

	unitest_replay <NODE_NAME> <testXX>

The outputs are available in the file testXX/output.tsv
