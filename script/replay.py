#!/usr/bin/env python3

import ast
import json
import os
import struct

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

struct_map = {
	"real" : 'f',
	"integer" : 'i',
	"boolean" : 'b',
	"pointer" : 'P',
}

DISABLED_CODE !!!

unitest_dir = Path(os.environ["UNITEST_root_DIR"])

def prepare_input(node_name, replay_no) :
	replay_dir = unitest_dir / "build" / node_name / "replay" / replay_no
	scade_map = json.loads((replay_dir / "../info.json").read_text())
	m = get_struct(scade_map["input"])
	value_lst = load_tsv(replay_dir / "input.tsv")
	stack = list()
	print("RAAAAH")
	for value in value_lst :
		line = m.pack(* value)
		if len(line) % 4 != 0 :
			line = line + b'\x00' * (((len(line) // 4) + 1) * 4) - len(line))
		stack.append(line)
	(replay_dir / "input.reb").write_bytes(b''.join(stack))
	
def load_binary(pth, info) :
	
	m = get_struct(info)
	h = sorted('.'.join(member).replace('*.', '.') for ctype, member in info)
		
	value_map = {
		k : list() for k in h
	}
	
	with pth.open('rb') as fid :
		while True :
			try :
				for n, v in enumerate(m.unpack(fid.read(m.size))) :
					value_map[h[n]].append(v)					
			except struct.error :
				break
				
	for k in value_map :
		value_map[k] = np.array(value_map[k])
				
	return value_map


def analyze_rec(node, replay="01") :
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
	
def plot_all(node_name, replay_no) :
	replay_dir = unitest_dir / node_name / "replay" / replay_no
	scade_map = json.loads((replay_dir / "../info.json").read_text())
	
	input_map = load_binary(replay_dir / "input.reb", scade_map["input"])
	for k in sorted(input_map) :
		plt.figure()
		plt.plot(input_map[k])
		plt.title(k)
		print("plot>", k)
		plt.savefig(str(replay_dir / "{0}.png".format(k)))
		
	full_map = load_binary(replay_dir / "full.reb", scade_map["full"])
	for k in (replay_dir / '../plot.default.tsv').read_text().splitlines() :
		if k.startswith('#') :
			continue
		plt.figure()
		plt.plot(full_map[k])
		plt.title(k)
		print("plot>", k)
		plt.savefig(str(replay_dir / "{0}.png".format(k)))	
		
	if (replay_dir / "reference.reb").is_file() :
		reference_map = load_binary(replay_dir / "reference.reb", scade_map["output"])
	experimental_map = load_binary(replay_dir / "output.reb", scade_map["output"])
	for k in sorted(experimental_map) :
		plt.figure()
		if (replay_dir / "reference.reb").is_file() :
			plt.plot(reference_map[k], linewidth=7, color='lightgray')
			s = 100.0 * np.sqrt(np.sum((reference_map[k] - experimental_map[k]) ** 2)) / len(reference_map[k])
		else :
			s = 0.0
		plt.plot(experimental_map[k])
		plt.title(k + " - {0}".format(s))
		print("plot>", k)
		plt.savefig(str(replay_dir / "{0}.png".format(k)))
		plt.close()

def get_struct(var_lst) :
	fmt = ''.join(struct_map[ctype] for ctype, member in var_lst)
	return struct.Struct(fmt)

def load_tsv(pth) :
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
			
	Path("input.first_pass.tsv").write_text('\n'.join(line_lst))
		
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
		
	Path("input.second_pass.tsv").write_text('\n'.join(str(i) for i in value_lst))
		
	return value_lst
	
if __name__ == '__main__' :

	#analyze_rec()
	#plot_all()
	import sys
	
	verb, node_name, replay_no = sys.argv[1:]
	
	if verb == "prepare" :
		prepare_input(node_name, replay_no)		
	if verb == "analyze" :
		plot_all(node_name, replay_no)		
		
	
	#info = load_tsv(Path(sys.argv[1]))
	#fmt = ''.join(scade_to_struct[i] for i in info["type"])
	#s = struct.Struct(fmt)
	#print(fmt)