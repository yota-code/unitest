#!/usr/bin/env python3

import re
import sys

from pathlib import Path

comment_rec = re.compile(r'\/\*.*?\*\/', re.DOTALL | re.MULTILINE)
multiline_rec = re.compile(r'\n\n+')

def clean_file(pth) :
	print("cleaning source file:{0}".format(pth))
	txt = pth.read_text(encoding='latin1')
	# if pth.suffix == '.h' :
	# 	txt = comment_rec.sub('', txt)
	txt = txt.replace('    ', '\t')
	txt = txt.replace(')\n{', ') {')
	txt = multiline_rec.sub('\n\n', txt)
	txt = txt.strip()
	txt = txt + '\n'
	pth.write_text(txt, encoding='utf8')	

def clean_folder(fld) :
	for pth in fld.rglob('*.c') :
		clean_file(pth)
	for pth in fld.rglob('*.h') :
		clean_file(pth)
	
if __name__ == "__main__" :
	
	pth_lst = [Path(arg) for arg in sys.argv[1:]]
	if not pth_lst :
		pth_lst.append(Path('.'))
	
	for pth in pth_lst :
		if pth.is_file() and pth.suffix in [".c", ".h"] and pth.resolve().parts[-2] == "scade" :
			clean_file(pth)
		elif pth.is_dir() and pth.resolve().parts[-1] == "scade" :
			clean_folder(pth)
