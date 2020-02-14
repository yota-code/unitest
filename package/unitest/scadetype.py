#!/usr/bin/env python3

import re

class ScadeType() :
	rec_struct = re.compile("""typedef\s+struct\s*\\{(?P<content>.*?)\\}\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*;""", re.MULTILINE | re.DOTALL)
	rec_typedef = re.compile("""typedef\s+(?P<old>.*?)\s+(?P<new>[a-zA-Z_][a-zA-Z0-9_]*)\s*;""")

	direct_map = {
		'float' : 'real',
		'_Bool' : 'boolean',
		'int_' : 'integer',
		'signed int' : 'integer',
		'int32_t' : 'integer',
		'void *' : 'pointer',
	}	
	
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
					yield _tree + [member[0], member[1] + ' *']
		else :
			yield _tree + [self.solve(name),]
			
	def clean(self, line) :
		ctype = self.direct_map.get(line[-1], line[-1])
		member = ['_C_*',] + [(i.lstrip('*') + '*' if i.startswith('*') else i) for i in line[1:-1]]
		return (ctype, ".".join(member).replace('*.', '->').rstrip('*'))
			
class ScadeStruct() :
	rec_member = re.compile(r'(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)\s+(?P<name>(\*\s*)?[a-zA-Z_][a-zA-Z0-9_]*)\s*;')
	
	def __init__(self) :
		self.member_list = list()
		
	def load_str(self, block) :
		for res in self.rec_member.finditer(block) :
			self.member_list.append((res.group('name'), res.group('type')))
		return self
		
