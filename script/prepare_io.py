#!/usr/bin/env python3

import argparse
import json
import pickle
import sys
import re

from pathlib import Path

DISABLED !!!

class ScadeType() :
	rec_struct = re.compile("""typedef\s+struct\s*\\{(?P<content>.*?)\\}\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*;""", re.MULTILINE | re.DOTALL)
	rec_typedef = re.compile("""typedef\s+(?P<old>.*?)\s+(?P<new>[a-zA-Z_][a-zA-Z0-9_]*)\s*;""")
	
	def __init__(self) :
		self.struct = dict()
		self.pool = dict()
		
	def load(self, pth) :
		if pth.suffix != '.i' :
			raise ValueError("Invalid file type")
		src = pth.read_text()
		src = '\n'.join([line for line in src.splitlines() if not line.startswith('#')])
		for res in self.rec_struct.finditer(src) :
			self.struct[res.group('name')] = ScadeStruct().load_str(res.group('content'))
		for res in self.rec_typedef.finditer(src) :
			try :
				self.struct[res.group('new')] = self.struct[res.group('old')]
			except KeyError :
				self.pool[res.group('new')] = res.group('old')
		return self
		
	def solve(self, type_name) :
		while True :
			if type_name in self.pool :
				type_name = self.pool[type_name]
			else :
				return type_name
				
	def to_tsv(self, root, alignement=8) :
		addr = 0
		stack = list()
		for line in self.walk(root) :
			url = '.'.join(line[:-1]).replace('.*', '.')
			typ = line[-1]
			d = {'void *' : 8, 'float' : 4, 'int32_t' : 4, '_Bool' : 1}[typ]
			if d == 8 :
				while addr % 8 != 0 :
					addr += 1
			elif d == 4 :
				while addr % 4 != 0 :
					addr += 1
			stack.append([addr, url, typ])
			addr += d
		return stack
	
	def walk(self, name, _tree=None, follow_pointer=False) :
		if _tree is None :
			_tree = ['_C_',]
		if name in self.struct :
			for member in self.struct[name].member_list :
				if follow_pointer or member[0][0] != '*' :
					for sub in self.walk(member[1], _tree + [member[0],], follow_pointer) :
						yield sub
				else :
					yield _tree + [member[0], 'void *']
		else :
			yield _tree + [self.solve(name),]
		
class ScadeStruct() :
	rec_member = re.compile(r'(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)\s+(?P<name>(\*\s*)?[a-zA-Z_][a-zA-Z0-9_]*)\s*;')
	
	def __init__(self) :
		self.member_list = list()
		
	def load_str(self, block) :
		for res in self.rec_member.finditer(block) :
			self.member_list.append((res.group('name'), res.group('type')))
		return self
		
def clean(line) :
	
	direct_map = {
		'float' : 'real',
		'_Bool' : 'boolean',
		'int_' : 'integer',
		'int32_t' : 'integer',
		'void *' : 'pointer',
	}	
	
	
	ctype = direct_map[line[-1]]
	member = ['_C_*',] + [(i[1:] + '*' if i.startswith('*') else i) for i in line[1:-1]]
	return (ctype, member)
		
if __name__ == '__main__' :
	
	ctype_map = {
		'real' : 'float',
		'boolean' : 'int8_t',
		'integer' : 'int32_t',
		'pointer' : 'void *',
	}
	
	stype_map = {
		"real" : 'f',
		"integer" : 'i',
		"boolean" : 'i',
		"pointer" : 'P',
	}
	
	header_pth = Path(sys.argv[1])
	
	node_name = header_pth.stem
	
	scadetype = ScadeType().load(header_pth)
	
	output_lst = list()
	input_lst = list()
	full_lst = list()
	for p in scadetype.walk('_C_' + node_name, follow_pointer=True) :
		if re.match(r'^\*?_I[0-9]+_', p[1]) :
			input_lst.append(clean(p))
		if re.match(r'^\*?_O[0-9]+_', p[1]) :
			output_lst.append(clean(p))
	for p in scadetype.walk('_C_' + node_name, follow_pointer=False) :
		full_lst.append(clean(p))

	#m = {'input': input_lst, 'output': output_lst}
	#with Path("../replay/info.json").open('wt') as fid :
	#	json.dump(m, fid, indent="\t")
		
	Path("../replay/plot.default.tsv").write_text(
		'\n'.join(('# ' + (".".join(member).replace('*.', '->'))) for ctype, member in full_lst if ctype != 'pointer')
	)
	
	Path("../replay/001/input.tsv").write_text('#' + '\t'.join([".".join(member).replace('*.', '->') for ctype, member in input_lst]))
	Path("../replay/001/initial.default.tsv").write_text('\n'.join((".".join(member).replace('*.', '->') + '\t') for ctype, member in input_lst))

	stack = list()
	w = stack.append
	w('#include "unitest_interface.h"')
	w('\n_C_{0} unitest_C_ = {{0}};'.format(node_name))
	for member, ctype in scadetype.struct['_C_' + node_name].member_list :
		if member.startswith('*') :
			w('{0} unitest_C_{1};'.format(ctype, member.lstrip('*')))
	w('\nint unitest_input_proc(_C_{0} * _C_, unitest_input_T * data) {{\n'.format(node_name))
	for n, (ctype, member) in enumerate(input_lst) :		
		w("\t{0} = data->_m_{2};".format(".".join(member).replace('*.', '->'), ctype, n))
	w('\n\treturn EXIT_SUCCESS;\n}\n')
	
	w('\nint unitest_output_proc(unitest_output_T * data, _C_{0} * _C_) {{\n'.format(node_name))
	for n, (ctype, member) in enumerate(output_lst) :
		w("\tdata->_m_{1} = {2};".format(ctype, n, ".".join(member).replace('*.', '->')))
	w('\n\treturn EXIT_SUCCESS;\n}\n')
	
	w('\nint unitest__init__(_C_{0} * _C_) {{\n'.format(node_name))
	for member, ctype in scadetype.struct['_C_' + node_name].member_list :
		if member.startswith('*') :
			w('\t_C_->{0} = & unitest_C_{0};'.format(member.lstrip('*')))
	w('\n\treturn EXIT_SUCCESS;\n}\n')

	Path("./source/unitest_interface.c").write_text('\n'.join(stack))
	
	stack = list()
	w = stack.append
	w('#ifndef __INCLUDE_unitest_interface_H')
	w('#define __INCLUDE_unitest_interface_H\n')
	w('#include "scade_types.h"')
	w('#include "{0}.h"\n'.format(node_name))
	w('#define UNITEST_NODE {0}\n'.format(node_name))
	w('\ntypedef struct {')
	for n, (ctype, member) in enumerate(input_lst) :		
		w("\t{1} _m_{2};".format(".".join(member).replace('*.', '->'), ctype_map[ctype], n))	
	w('} unitest_input_T;')
	w('\ntypedef struct {')
	for n, (ctype, member) in enumerate(output_lst) :		
		w("\t{1} _m_{2};".format(".".join(member).replace('*.', '->'), ctype_map[ctype], n))	
	w('} unitest_output_T;')	
	w('\nint unitest_input_proc(_C_{0} * _C_, unitest_input_T * data) ;'.format(node_name))
	w('int unitest_output_proc(unitest_output_T * data, _C_{0} * _C_) ;'.format(node_name))
	w('\nint unitest__init__(_C_{0} * _C_) ;'.format(node_name))
	w('\nextern _C_{0} unitest_C_;'.format(node_name))
	for member, ctype in scadetype.struct['_C_' + node_name].member_list :
		if member.startswith('*') :
			w('extern {0} unitest_C_{1};'.format(ctype, member.lstrip('*')))	
	w('\n#endif /* __INCLUDE_unitest_interface_H */\n')

	Path("./include/unitest_interface.h").write_text('\n'.join(stack))
	
	unitest_input_lst = list()
	unitest_input_set = set()
	for n, (stype, sname) in enumerate(input_lst) :
		if sname[1].endswith('*') :
			unitest_input_set.add(sname[1][:-1])
	
			
	print(unitest_input_set)
	sys.exit(0)
	
	txt = Path("../main.c").read_text()
	txt = txt.replace("##UNITEST_NODE##", node_name)
	Path("../main.c").write_text(txt)
	
	stack = list()
	for ctype, member in m['full'] :
		key = ".".join(member).replace('*.', '->')
		var = key.replace('_C_.', 'unitest_C_.').rstrip('*')
		stack.append(
			'\tprintf("{0}\\t{1}\\t%ld\\n", ((size_t) &({2})) - ((size_t) &(unitest_C_)));'.format(key, ctype, var)
		)
	                                                             
	txt = Path("../../__template__/full_mapping.c").read_text()
	txt = txt.replace("##UNITEST_NODE##", node_name)
	txt = txt.replace("##UNITEST_MAP##", '\n'.join(stack))
	Path("../full_mapping.c").write_text(txt)	

	#txt = Path("../closed_loop.c").read_text()
	#txt = txt.replace("##UNITEST_NODE##", node_name)
	#Path("../closed_loop.c").write_text(txt)

