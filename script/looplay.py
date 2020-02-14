#!/usr/bin/env python3

import ast
import json
import os
import re
import struct
import subprocess
import sys

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

unitest_dir = Path(os.environ["AUTOPILOT_unitest_DIR"]).resolve()

class LooPlay() :
	
	struct_map = {
		"real" : 'f',
		"integer" : 'i',
		"boolean" : 'i',
		"pointer" : 'P',
	}	
	
	def __init__(self, unitest_dir, node_name, replay_no) :
		self.unitest_dir = unitest_dir
		self.node_name = node_name
		self.replay_no = replay_no
		
		self.scade_map = json.loads((self.replay_dir / "../info.json").read_text())
		
	def get_typedef(self, way) :
		return struct.Struct(
			''.join(self.struct_map[ctype] for ctype, member in self.scade_map[way])
		)
		
	def get_varlist(self, way) :
		return sorted(
			'.'.join(member).replace('*.', '->') for ctype, member in self.scade_map[way]
		)		
		
	@property
	def replay_dir(self) :
		return self.unitest_dir / self.node_name / "replay" / self.replay_no
		
	@property
	def node_dir(self) :
		return self.unitest_dir / self.node_name
		
	def prepare_input(self) :
		typedef = self.get_typedef("input")
		value_lst = load_tsv(self.replay_dir / "input.tsv")
		stack = list()
		for value in value_lst :
			stack.append(typedef.pack(* value))
		(replay_dir / "input.reb").write_bytes(b''.join(stack))
	
	def prepare_initial(self) :
		typedef = self.get_typedef("input")
		value_lst = list()
		for line in (self.replay_dir / "initial.tsv").read_text().splitlines() :
			key, value = line.split('\t')
			value_lst.append(ast.literal_eval(value.strip()))
		(replay_dir / "input.reb").write_bytes(typedef.pack(* value_lst))
		
	def read_variable(self, key) :
		line_lst = (self.node_dir / "mapping.tsv").read_text().splitlines()
		sizeof = int(line_lst.pop(0))
		full_map = dict()
		for line in line_lst :
			k, ctype, size = line.split('\t')
			full_map[k] = [ctype, int(size)]
		full_reb = self.replay_dir / "full.reb"
		ctype, offset = full_map[key]
		stack = list()
		with full_reb.open('rb') as fid :
			block = fid.read(sizeof)
			while len(block) == sizeof :
				stack.append(struct.unpack_from(self.struct_map[ctype], block, offset)[0])
				block = fid.read(sizeof)
		return np.array(stack)
				
	def load_io(self, way, alternate_file=None) :
		typedef = self.get_typedef(way)
		varlist = self.get_varlist(way)
		value_map = { k : list() for k in varlist }
		with (replay_dir / "{0}.reb".format(way if alternate_file is None else alternate_file)).open('rb') as fid :
			while True :
				try :
					for n, v in enumerate(typedef.unpack(fid.read(typedef.size))) :
						value_map[varlist[n]].append(v)					
				except struct.error :
					break
		for k in value_map :
			value_map[k] = np.array(value_map[k])
		return value_map
		
	def plot_one(self, data, title) :
		plt.figure()
		plt.plot(data)
		plt.title(title)
		print("plot >", title)
		plt.savefig(str(replay_dir / "{0}.png".format(''.join(c for c in title if re.match(r'\w', c)))))
		plt.close()
		
	def plot_all(self) :
		for pth in self.replay_dir.glob('*.png') :
			pth.unlink()
			
		input_map = self.load_io("input")
		for k in sorted(input_map) :
			if 'S_Param' in k :
				continue
			self.plot_one(input_map[k], k)
		
		reference_reb = self.replay_dir / "reference.reb"
		if reference_reb.is_file() :
			reference_map = self.load_io("output", "reference")
		
		experimental_reb = self.replay_dir / "output.reb"
		experimental_map = self.load_io("output")
		for k in sorted(experimental_map) :
			plt.figure()
			if reference_reb.is_file() :
				plt.plot(reference_map[k], linewidth=7, color='lightgray')
				s = 100.0 * np.sqrt(np.sum((reference_map[k] - experimental_map[k]) ** 2)) / len(reference_map[k])
			else :
				s = 0.0
			plt.plot(experimental_map[k])
			plt.title(k + " - {0}".format(s))
			print("plot >", k)
			plt.savefig(str(replay_dir / "{0}.png".format(''.join(c for c in k if re.match(r'\w', c)))))
			plt.close()
		
		if (replay_dir / '../plot.tsv').is_file() :
			plot_lst = (replay_dir / '../plot.tsv').read_text().splitlines()
			# full_map = load_binary(replay_dir / "full.reb", scade_map["full"])
			
			for k in sorted(plot_lst) :
				if k.startswith('#') :
					continue
				data = self.read_variable(k)
				self.plot_one(data, k)


def analyze_rec(node="q_TrajGenerator2", replay="001") :
	replay_dir = unitest_dir / node / "replay" / replay
	
	scade_map = json.loads((replay_dir / "../info.json").read_text())
	
	m = get_struct(scade_map["output"])
	
	with (replay_dir / "replay.rec").open('rb') as fid :
		value_lst = list()
		while True :
			try :
				value_lst.append(list(m.unpack(fid.read(m.size))))
			except struct.error :
				break
				
	print(load_binary(replay_dir / "replay.rec", scade_map["output"]))
				
	(replay_dir / "output.tsv").write_text(
		'\n'.join('\t'.join(str(i) for i in value) for value in value_lst)
	)
	

	


	
if __name__ == '__main__' :
	
	length, node_name, replay_no = sys.argv[1:]
	
	replay_dir = unitest_dir / node_name / "replay" / replay_no
	
	length = int(length)
	sys.path += [str(replay_dir),]
	
	print((unitest_dir / node_name))
	print((unitest_dir / node_name /  'main.exe').is_file())

	
	import closeloop
	
	u = closeloop.Block(replay_dir)
	p = LooPlay(unitest_dir, node_name, replay_no)
	
	p.prepare_initial()	
	for n in range(length) :
		subprocess.run("../../main.exe", cwd=replay_dir)
		u.run(n)
		
	u.plot()		
		
