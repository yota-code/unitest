SHELL=/usr/bin/env sh

PREFIX=$(CURDIR)

target_TAG:=$(shell hostname)

project_DATE:=$(shell date +"%Y-%m-%d %H:%M")
project_TAG:=unitest
	
source_to_object=$(addprefix $(2)/,$(patsubst %.c,%.o,$(notdir $(1))))
	
CC:=gcc
CFLAGS:= \
	-std=c99 -pedantic -Wall -Winline -g \
	-fPIC -fno-strict-aliasing -O2 -DUNITEST_MODE -D_GNU_SOURCE \
	-I$(PREFIX)/include -I$(PREFIX)/include/scade -I$(PREFIX)/include/fctext
	
tmp_DIR:=$(PREFIX)/build/$(target_TAG)/tmp
lib_DIR:=$(PREFIX)/build/$(target_TAG)/lib
bin_DIR:=$(PREFIX)/build/$(target_TAG)/bin

.PHONY: preface postface create_dir clean all scade_lib fctext_lib unitest_lib

all: preface executable postface

###  scade  ####################################################################################

scade_DIR:=$(PREFIX)/src/scade
scade_SRC:=$(wildcard $(scade_DIR)/*.c)
scade_TMP:=$(tmp_DIR)/src/scade
scade_OBJ:=$(call source_to_object,$(scade_SRC),$(scade_TMP))
scade_LIB:=$(lib_DIR)/libscade.a

scade_lib: $(scade_LIB)

$(scade_TMP)/%.o: $(scade_DIR)/%.c
	@echo "scade 1. $(notdir $@)"
	@$(CC) -c $(CFLAGS) $< -o $@

$(scade_LIB): $(scade_OBJ)
	@echo "scade 2. $(notdir $@)"
	@ar rs $(scade_LIB) $? 2> /dev/null
	
###  unitest  ####################################################################################

unitest_DIR:=$(PREFIX)/src/unitest
unitest_SRC:=$(wildcard $(unitest_DIR)/*.c)
unitest_TMP:=$(tmp_DIR)/src/unitest
unitest_OBJ:=$(call source_to_object,$(unitest_SRC),$(unitest_TMP))
unitest_LIB:=$(lib_DIR)/libunitest.a

unitest_lib: $(unitest_LIB)

$(unitest_TMP)/%.o: $(unitest_DIR)/%.c
	@echo "unitest 1. $(notdir $@)"
	@$(CC) -c $(CFLAGS) $< -o $@

$(unitest_LIB): $(unitest_OBJ)
	@echo "unitest 2. $(notdir $@)"
	@ar rs $(unitest_LIB) $? 2> /dev/null
	
###  fctext  ####################################################################################

fctext_DIR:=$(PREFIX)/src/fctext
fctext_SRC:=$(wildcard $(fctext_DIR)/*.c)
fctext_TMP:=$(tmp_DIR)/src/fctext
fctext_OBJ:=$(call source_to_object,$(fctext_SRC),$(fctext_TMP))
fctext_LIB:=$(lib_DIR)/libfctext.a

fctext_lib: $(fctext_LIB)

$(fctext_TMP)/%.o: $(fctext_DIR)/%.c
	@echo "fctext 1. $(notdir $@)"
	@$(CC) -c $(CFLAGS) $< -o $@

$(fctext_LIB): $(fctext_OBJ)
	@echo "fctext 2. $(notdir $@)"
	@ar rs $(fctext_LIB) $? 2> /dev/null
	
###  executable  ###############################################################################

executable: $(fctext_LIB) $(scade_LIB) $(unitest_LIB)
	@echo "building executable"
	@$(CC) $(CFLAGS) main.c -I. $(fctext_OBJ) $(scade_OBJ) $(unitest_OBJ) -lm -o main.exe
	
###  other  ####################################################################################

preface: create_dir
	@echo -e "\n>>>  BUILD  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  $(project_DATE)  >>>\n"
	@echo -e "\tproject: $(project_TAG)\n"
	@echo -e "\ttarget: $(target_TAG)"
	@echo -e "\n=====================================================================\n"

postface:
	@echo -e "\n=====================================================================\n"
	@echo -e "products:"
	@echo -e "\t$(scade_LIB)"
	@echo -e "\n<<<  $(target_TAG)  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  END  <<<\n"

create_dir:
	@mkdir --parents $(tmp_DIR)
	@mkdir --parents $(lib_DIR)
	@mkdir --parents $(bin_DIR)
	@mkdir --parents $(scade_TMP)
	@mkdir --parents $(fctext_TMP)
	@mkdir --parents $(unitest_TMP)

clean:
	-@rm --recursive --force $(tmp_DIR)
	-@rm $(fctext_LIB) $(scade_LIB) $(unitest_LIB)
	@echo -e "\ncleaned ... \n"
