#!/usr/bin/env python3

import os

import mako.template

from cc_pathlib import Path

w_dir = Path(os.environ['UNITEST_working_DIR'])

def unroll_file(src_dir, src_pth, dst_dir, arg_nam) :
	#print("unroll_template_file({0}, {1}, {2}, {3})".format(src_dir, src_pth, dst_dir, arg_nam))
	src_pth = (src_dir / src_pth)
	if src_pth.is_file() :
		if src_pth.suffix == ".mako" :
			m = mako.template.Template(filename=str(src_pth), module_directory=str(w_dir / '.mako_tmp'))
			dst_pth = (dst_dir / src_pth.relative_to(src_dir)).with_suffix('')
			# print("MAKO :: {0}\n     -> {1}".format(src_pth, dst_pth))
			dst_pth.parent.mkdir(parents=True, exist_ok=True)
			try :
				dst_pth.write_text(m.render(** arg_nam))
			except Exception as e :
				dst_pth.write_text(f'Failed rendering ! {e}\n------\n{traceback.format_exc()}')
		else :
			dst_pth = (dst_dir / src_pth.relative_to(src_dir))
			# print("COPY :: {0}\n     -> {1}".format(src_pth, dst_pth))
			dst_pth.parent.mkdir(parents=True, exist_ok=True)
			dst_pth.write_bytes(src_pth.read_bytes())
	else :
		raise ValueError("not a valid .mako file:{0}".format(src_dir / src_pth))

def unroll_folder(src_dir, dst_dir, arg_nam, src_root=None, dst_root=None) :
	# print("unroll_template_folder({0}, {1}, {2}, {3})".format(src_dir, dst_dir, arg_nam, src_root))

	if src_root is None :
		src_root = src_dir
	if dst_root is None :
		dst_root = dst_dir

	for pth in src_dir.iterdir() :
		if pth.name.startswith('.') :
			continue
		if pth.is_file() :
			print("FILE :: {0}".format(pth))
			print("---", pth)
			unroll_file(src_root, pth.relative_to(src_root), dst_root, arg_nam)
		if pth.is_dir() :
			# print("FOLDER :: {0}".format(pth))
			unroll_folder(pth, dst_dir / pth.relative_to(src_root), arg_nam, src_root, dst_root)
