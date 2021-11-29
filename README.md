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
	ln -snf /C/autools/zprofile/zshrc .zshrc 

Create if needed your personal folder on \\nahar\fdat1038\source\ with aXXXXX (or echo $(whoami))

	cd /C/autools/source/
	mkdir $(whoami)

Install unitest in your folder on \\nahar\fdat1038\source\aXXXX via git clone
URL http://sma6299.eu.eurocopter.corp/gitea/ETGGC/unitest
* either use it on unix via

	cd /C/autools/source/$(whoami)/
	git clone http://sma6299.eu.eurocopter.corp/gitea/ETGGC/unitest
	
* either on windows via TortoiseGit using the option Git / Global / AutoCrLf at false and the Git Clone http://sma6299.eu.eurocopter.corp/gitea/ETGGC/unitest

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

	unitest_prepare <NODE_NAME> <template>

With as template scade_v3 / scade_mini / helionix

Remark : the unitest environment is located in the folder build/<NODE_NAME>

# How to start a simulation

Create a test folder in build/<NODE_NAME>/replay

	mkdir testXX

From the folder build/<NODE_NAME>/replay/testXX, copy the file inputs.tsv (scenario) in the folder and modify it, (variable modification / addition of lines)

Start the scenario for the node

	unitest_replay <NODE_NAME> <testXX>

The outputs are available in the file testXX/output.tsv

# Errors

If your models do not use a table1, the type should be manually added in your unitest/kcg/<NODE_NAME>/scade_type.h
typedef struct {
real _F0;
real _F1;
real _F2;
real _F3;
real _F4;
real _F5;
real _F6;
real _F7;
real _F8;
real _F9;
real _F10;
real _F11;
real _F12;
real _F13;
real _F14;
real _F15;
real _F16;
real _F17;
real _F18;
real _F19;
} _T<number_type+1>_<NODE_NAME>;

typedef _T<number_type+1>_<NODE_NAME> intpol_vec;

typedef struct {
intpol_vec Point_Arg;
intpol_vec Point_Val;
_int Bound;
} _T<number_type+2>_<NODE_NAME>;

typedef _T<number_type+2>_<NODE_NAME> table1;