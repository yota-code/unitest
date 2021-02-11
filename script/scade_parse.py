#!/usr/bin/env python3

""" 
take a preprocessed source, obtained with `gcc -E *.c` as input
dump a list of all variables of the structure tree.
designed mainly for scade_type.h patterns.
"""

import argparse
import json
import pickle
import sys
import re

from pathlib import Path

class ScadeType() :
	rec_struct = re.compile("""typedef\s+struct\s*\\{(?P<content>.*?)\\}\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*;""", re.MULTILINE | re.DOTALL)
	rec_typedef = re.compile("""typedef\s+(?P<old>.*?)\s+(?P<new>[a-zA-Z_][a-zA-Z0-9_]*)\s*;""")
	
	def __init__(self) :
		self.struct = dict()
		self.pool = dict()
		
	def load(self, pth) :
		if pth.suffix != '.h' :
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
		#prev = None
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
			#if prev is not None and prev != ''.join(line[:-2]) :
			#	while addr % 8 != 0 :
			#		addr += 1
			#prev = ''.join(line[:-2])
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
				
def zpickle_dump(pth, obj) :
	import pickle
	import gzip
	
	with gzip.open(str(pth), 'wb') as fid :
		pickle.dump(obj, fid)
		
def zpickle_load(pth) :
	import pickle
	import gzip
	
	with gzip.open(str(pth), 'rb') as fid :
		obj = pickle.load(fid)
	return obj

if __name__ == '__main__' :
	
	pa = argparse.ArgumentParser("pre-process a header file")
	pa.add_argument('header', metavar="FILE", type=Path)
	pa.add_argument('--root', type=str)
	
	ap = pa.parse_args()
			
	u = ScadeType().load(ap.header)
	
	#zpickle_dump(ap.header.with_suffix('.meta'), u)
	#
	ap.header.with_suffix('.json').write_text(json.dumps(list(u.walk('_C_' + ap.root))))
	#
	ap.header.with_suffix('.tsv').write_text(
		'\n'.join(
			'\t'.join(str(cell) for cell in line)
			for line in u.to_tsv('_C_' + ap.root)
		)
	)
	
	stack = list()
	for (n, m, t) in u.to_tsv('_C_' + ap.root) :
		stack.append('\tprintf("%ld\\t{1}\\t{2}\\n", (void *)(& ({1})) - (void *)(& _C_));'.format(n, m, t))
	
	txt = Path("debug.c.__template__").read_text()
	txt = txt.replace("###NAME###", ap.root)
	txt = txt.replace("###TEMPLATE###", "\n".join(stack))
	Path("debug.c").write_text(txt)
		
		
	
