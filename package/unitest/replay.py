#!/usr/bin/env python3

import ast
import collections
import os
import struct
import subprocess

import numpy as np

from cc_pathlib import Path

import structarray

def to_str(s) :
	if isinstance(s, int) :
		return '{0}'.format(s)
	if isinstance(s, float) :
		return '{0:0.5g}'.format(s)
	else :
		return str(s)

class UnitestReplay() :
	
	struct_map = {
		"R4" : 'f',
		"R8" : 'd',
		"Z4" : 'i',
		"B4" : 'i',
		"P4" : 'P',
		"Z1" : 'b'
	}
	
	def __init__(self, node_name, replay_no) :
		self.node_name = node_name
		self.replay_no = replay_no
		
		self.node_dir = Path(os.environ["UNITEST_build_DIR"]).resolve() / node_name
		self.replay_dir = self.node_dir / "replay" / replay_no
		
		self.load_io()
		
		self.data_len = None
		self.data_pth = self.replay_dir / "context.reb"
		
	def load_io(self) :
		self.input_lst = (self.node_dir / "mapping" / "input.tsv").load()
		self.input_fmt = self.get_struct(self.input_lst)
		print(f"P sizeof(unitest_input_T) = {self.input_fmt.size} x {len(self.input_lst)} -- {self.input_fmt.format}")

		self.output_lst = (self.node_dir / "mapping" / "output.tsv").load()
		self.output_fmt = self.get_struct(self.output_lst)
		print(f"P sizeof(unitest_output_T) = {self.output_fmt.size} x {len(self.output_lst)} -- {self.output_fmt.format}")

	def get_struct(self, var_lst) :
		fmt = ''.join(self.struct_map[ctype] for name, ctype in var_lst)
		return struct.Struct(fmt)
		
	def dump_output(self) :
		stack = [
			[c[0] for c in self.output_lst],
		]
		
		with (self.replay_dir / "output.reb").open('rb') as fid :
			block = fid.read(self.output_fmt.size)
			while len(block) == self.output_fmt.size :		
				stack.append(self.output_fmt.unpack(block))
				block = fid.read(self.output_fmt.size)
		(self.replay_dir / "output.tsv").save(stack)
	
	def prepare_trajectory(self) :
		value_lst = self.load_trajectory(self.replay_dir / "input.tsv")
		stack = list()
		for value in value_lst :
			line = self.input_fmt.pack(* value)
			if len(line) % 4 != 0 :
				line = line + b'\x00' * ((((len(line) // 4) + 1) * 4) - len(line))
			stack.append(line)
		(self.replay_dir / "input.reb").write_bytes(b''.join(stack))
		
	def load_trajectory(self, pth) :
		txt = pth.read_text().splitlines()
		
		line_lst = list()
		for line in txt :
			if line.startswith('#') :
				continue
			if line.startswith('x') and '!' not in line :
				x = int(line.lstrip('x'))
				for i in range(x) :
					line_lst.append(line_lst[-1])
			else :
				line_lst.append(line)
		
		(self.replay_dir / "input.first_pass.tsv").write_text('\n'.join(line_lst))
			
		value_lst = list()
		for line in line_lst :
			line_lst = list()
			for n, i in enumerate(line.split('\t')) :
				i = i.strip()
				if line.startswith('!') :
					x = int(line.lstrip('!'))
					for i in range(x) :
						value_lst.append(value_lst[-1])
					continue
				if i and i != '.' :
					if i[0] == '+' :
						relative_mode = True
						i = i[1:]
					else :
						relative_mode = False
					p = ast.literal_eval(i)
					if relative_mode :
						p += value_lst[-1][n]				
				else :
					p = value_lst[-1][n]
				line_lst.append(p)
			if line_lst :
				value_lst.append(line_lst)
			
		(self.replay_dir / "input.second_pass.tsv").write_text('\n'.join(str(i) for i in value_lst))
			
		return value_lst
		
	def run_node(self) :
		subprocess.run('../../main.exe', cwd=self.replay_dir)
		
	def to_tsv(self) :

		u = structarray.StructArray(
			self.node_dir / "mapping" / "context.tsv",
			self.replay_dir / "context.reb",

		)
		u.to_tsv(self.replay_dir / "context.tsv")

		u.to_listing(self.replay_dir / "listing.tsv")

		return
		
	# def _load_meta(self, meta_pth) :
	# 	self.meta_pth = meta_pth

	# 	line_lst = self.meta_pth.read_text().splitlines()
	# 	self.name, sizeof = line_lst[0].split('\t')
	# 	self.sizeof = int(sizeof)
	# 	for line in line_lst[1:] :
	# 		name, ctype, offset = line.split('\t')
	# 		self.meta[name] = [ctype, int(offset)]
	# 	print("P sizeof(unitest_output_T) = {0}".format(self.sizeof))

	# 	return self

	# def _load_data(self) :
	# 	for name in self.meta :
	# 		self[name]
	# 	print(len(self.data))
	# 	return self
		
	# def __getitem__(self, name) :
	# 	if name not in self.data :
	# 		ctype, offset = self.meta[name]
	# 		stack = list()
	# 		with self.data_pth.open('rb') as fid :
	# 			block = fid.read(self.sizeof)
	# 			while len(block) == self.sizeof :
	# 				stack.append(struct.unpack_from(self.struct_map[ctype], block, offset)[0])
	# 				block = fid.read(self.sizeof)
	# 		self.data[name] = np.array(stack)
	# 		if self.data_len is not None and self.data_len != len(stack) :
	# 			raise ValueError("Inconsistent array")
	# 		self.data_len = len(stack)
	# 	return self.data[name]

	# def _dump_tsv(self) :
	# 	stack = list()
	# 	stack.append(list(self.data))
	# 	for i in range(self.data_len) :
	# 		stack.append([
	# 			to_str(self.data[k][i]) for k in self.data
	# 		])
	# 	print(self.data_len)
	# 	(self.replay_dir / "context.tsv").write_text('\n'.join('\t'.join(line) for line in stack))

		
if __name__ == '__main__' :
	u = UnitestReplay('q_TrajCanon2', "001")
	# u = UnitestReplay('integ', "002")
	u.prepare_trajectory()
	u.run_node()
	u.context_to_tsv()

	
	
	
