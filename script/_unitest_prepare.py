#!/usr/bin/env python3

import os
import subprocess
import sys

from cc_pathlib import Path

import structarray

import unitest

scade_context_template = '''#include <stdlib.h>
#include <stdio.h>

#include <string.h>

#define inttype_info(t) printf("\\t\\"%s\\" : \\"%s%d\\",\\n", #t, ( ( (((t)(0)) - 1) > 0) ? ("N") : ("Z")), sizeof(t))
#define realtype_info(t) printf("\\t\\"%s\\" : \\"%s%d\\",\\n", #t, "R", sizeof(t))
#define pointertype_info(t) printf("\\t\\"%s\\" : \\"%s%d\\",\\n", #t, "P", sizeof(t))

#include "scade_types.h"

#include "{node_name}.h"

_C_{node_name} context = {{0}};

int main(int argc, char * argv[]) {{

	printf("{{\\n");

	pointertype_info(void*);

	inttype_info(unsigned int);
	inttype_info(bool);
	inttype_info(signed char);
	inttype_info(unsigned char);
	inttype_info(short);
	inttype_info(int);
	inttype_info(long);
	inttype_info(long long);
	inttype_info(unsigned long);

	realtype_info(float);
	realtype_info(double);

	printf("}}\\n");

	memset(& context, 0, sizeof(_C_{node_name}));

	return EXIT_SUCCESS; 

}}
'''

scade_interface_template = '''#include <stdlib.h>
#include <stdio.h>

#include <string.h>

#include "unitest/interface.h"

unitest_input_T input = {0};
unitest_output_T output = {0};

int main(int argc, char * argv[]) {

	memset(& input, 0, sizeof(unitest_input_T));
	memset(& output, 0, sizeof(unitest_output_T));

	return EXIT_SUCCESS; 

}
'''

def map_context(node_name, include_lst) :

	cwd = Path(os.environ['UNITEST_build_DIR']) / node_name / "mapping"
	cwd.make_dirs()

	(cwd / 'structarray_context.c').write_text(scade_context_template.format(node_name=node_name))

	cmd = (
		["gcc", "-save-temps", "-std=c99", "-g"] +
		[f"-I{str(include_dir)}" for include_dir in include_lst] +
		["structarray_context.c", "-o", "structarray_context.exe"]
	)
	ret = cwd.run(* cmd)
	if ret.returncode != 0 :
		raise ValueError("gcc couldn't compile properly")

	ret = cwd.run("./structarray_context.exe")
	txt = ret.stdout.decode(sys.stdout.encoding)
	(cwd / "structarray_ctype.json").write_text(txt.replace(',\n}', '\n}'))

	u = structarray.StructInfo(cwd / 'structarray_context.exe')
	u.parse('context')
	u.save(cwd, 'context')

	return u

def map_interface(node_name, include_lst) :
	cwd = Path(os.environ['UNITEST_build_DIR']) / node_name / "mapping"
	cwd.make_dirs()

	(cwd / 'structarray_interface.c').write_text(scade_interface_template)

	cmd = (
		["gcc", "-save-temps", "-std=c99", "-g"] +
		[f"-I{str(include_dir)}" for include_dir in include_lst] +
		["structarray_interface.c", "-o", "structarray_interface.exe"]
	)
	ret = cwd.run(* cmd)
	if ret.returncode != 0 :
		raise ValueError("gcc couldn't compile properly")

	ret = cwd.run("./structarray_interface.exe")

	for k in ["input", "output"] :
		u = structarray.StructInfo(cwd / 'structarray_interface.exe')
		u.parse(k)
		u.save(cwd, k)

def unroll_tempate(node_name, template_name, context_info) :

	node_dir = Path(os.environ['UNITEST_build_DIR']) / node_name
	if not node_dir.is_dir() :
		raise ValueError("Not a valid model directory:{0}".format(node_dir))
	
	template_dir = Path(os.environ['UNITEST_template_DIR']) / template_name
	if not template_dir.is_dir() :
		raise ValueError("Not a valid template directory:{0}".format(template_dir))

	unitest.unroll_template_folder(template_dir, node_dir, {
		'scade_map' : context_info,
		'node_name' : node_name
	})


if __name__ == '__main__' :

	include_lst = [
		'../include',
		'../include/fctext',
		'../include/scade'
	]

	node_name = sys.argv[1]
	template_name = sys.argv[2]

	context_info = map_context(node_name, include_lst)
	unroll_tempate(node_name, template_name, context_info)
	map_interface(node_name, include_lst)