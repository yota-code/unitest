#!/usr/bin/env python3

import ast
import collections
import os
import struct
import subprocess

import numpy as np

from cc_pathlib import Path

import structarray.meta

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
		"Z1" : 'b',
		"N8" : 'L',
		"N4" : 'I',
		"N1" : 'B',
	}
	
	def __init__(self, node_name, replay_no) :
		self.node_name = node_name
		self.replay_no = replay_no
		
		self.node_dir = Path(os.environ["UNITEST_working_DIR"]).resolve() / "model" / node_name
		self.replay_dir = self.node_dir / "replay" / replay_no
		
		self.data_len = None
		self.data_pth = self.replay_dir / "context.reb"

	def run(self) :
		self.update_const()
		self.prep_input()

		self.run_node()

		# self.output_to_tsv()
		# self.context_to_tsv()
		self.link_to_last()

	def update_const(self) :
		for src_pth in self.replay_dir.glob('*.c') :
			dst_pth = self.node_dir / "src" / "fctext" / src_pth.name
			print(src_pth, dst_pth)
			dst_pth.write_bytes( src_pth.read_bytes() )
		for src_pth in self.replay_dir.glob('*.h') :
			dst_pth = self.node_dir / "include" / "fctext" / src_pth.name
			print(src_pth, dst_pth)
			dst_pth.write_bytes( src_pth.read_bytes() )

		self.node_dir.run("make")

	def prep_input(self) :
		self.input_sta = structarray.meta.MetaReb().load(
			self.node_dir / "mapping" / "input_map.tsv",
		)

		stack = list()
		for value_lst in self.load_trajectory(self.replay_dir / "input.tsv") :
			line = bytearray(self.input_sta.sizeof)
			for (name, mtype, offset), value in zip(self.input_sta, value_lst) :
				if mtype == 'Z4' :
					p = ( value & 0xFFFFFFFF )
					q = p if p < 0x80000000 else p - 0x100000000
					value = q
				try :
					struct.pack_into(self.struct_map[mtype], line, offset, value)
				except struct.error :
					print(f"struct.pack_into({mtype} / {self.struct_map[mtype]}, <line>, {offset}, {name} = {value})")
					raise
			stack.append(line)
		(self.replay_dir / "input.reb").write_bytes(b''.join(stack))

		# self.input_lst = (self.node_dir / "mapping" / "input.tsv").load()[1:]
		# self.input_fmt = struct.Struct(''.join(self.struct_map[ctype] for name, ctype in self.input_lst))

		# print(f"P sizeof(unitest_input_T) = {self.input_fmt.size} x {len(self.input_lst)} -- {self.input_fmt.format}")

		# self.prepare_trajectory()

		# return

		# self.output_lst = (self.node_dir / "mapping" / "output.tsv").load()
		# self.output_fmt = self.get_struct(self.output_lst)
		# print(f"P sizeof(unitest_output_T) = {self.output_fmt.size} x {len(self.output_lst)} -- {self.output_fmt.format}")

		
	# def dump_output(self) :
	# 	stack = [
	# 		[c[0] for c in self.output_lst],
	# 	]
		
	# 	with (self.replay_dir / "output.reb").open('rb') as fid :
	# 		block = fid.read(self.output_fmt.size)
	# 		while len(block) == self.output_fmt.size :		
	# 			stack.append(self.output_fmt.unpack(block))
	# 			block = fid.read(self.output_fmt.size)
	# 	(self.replay_dir / "output.tsv").save(stack)
	
	def prepare_trajectory__disabled__(self) :
		value_lst = self.load_trajectory(self.replay_dir / "input.tsv")
		stack = list()
		for value in value_lst :
			line = self.input_fmt.pack(* value)
			unit = 4
			if len(line) % unit != 0 :
				line = line + b'\x00' * ((((len(line) // unit) + 1) * unit) - len(line))
			stack.append(line)
		(self.replay_dir / "input.reb").write_bytes(b''.join(stack))
		
	def load_trajectory(self, pth) :
		txt = pth.read_text().splitlines()[1:]
		
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
		
		# (self.replay_dir / "input.first_pass.tsv").write_text('\n'.join(line_lst))
			
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
					if i in ['nan', 'inf', '+inf', '-inf'] :
						p = float(i)
					else :
						p = ast.literal_eval(i)
					if relative_mode :
						p += value_lst[-1][n]				
				else :
					p = value_lst[-1][n]
				line_lst.append(p)
			if line_lst :
				value_lst.append(line_lst)
			
		#print(value_lst)
		(self.replay_dir / "input_exp.tsv").save(value_lst)
			
		return value_lst
		
	def run_node(self) :
		subprocess.run('../../main.exe', cwd=self.replay_dir)
		
	def output_to_tsv(self) :
		u = structarray.StructArray(
			self.node_dir / "mapping" / "output.tsv",
			self.replay_dir / "output.reb",
		)
		u.to_tsv(self.replay_dir / "output.tsv")

	def context_to_tsv(self) :
		u = structarray.StructArray(
			self.node_dir / "mapping" / "context.tsv",
			self.replay_dir / "context.reb",
		)
		u.to_tsv(self.replay_dir / "context.tsv")
		u.to_listing(self.replay_dir / "listing.tsv", at=100)

	def link_to_last(self) :
		last_dir = (self.replay_dir / '../__last__').resolve()

		last_dir.make_dirs()
		for src_pth in self.replay_dir :
			dst_pth = last_dir / src_pth.name
			if dst_pth.is_file() :
				dst_pth.unlink()
			dst_pth.hardlink_to(src_pth)
		
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

	
	
	
