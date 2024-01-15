#!/usr/bin/env python3

import os
import shutil
import re

from cc_pathlib import Path

def scade_copy(src_pth, dst_pth) :

	ret = Path(src_pth.parent).run('gcc', '-fpreprocessed', '-dD', '-E', src_pth)
	txt = ret.stdout.decode('latin-1')
	
	txt = txt.replace('    ', '\t')
	txt = txt.replace(')\n{', ') {')
	txt = re.compile(r'\n\n+').sub('\n\n', txt)
	txt = txt.strip()
	txt = txt + '\n'

	dst_pth.write_text(txt)

class UnitestPrepare() :

	kcg_dir = Path(os.environ['UNITEST_kcg_DIR'])
	template_dir = Path(os.environ['UNITEST_template_DIR'])
	build_dir = Path(os.environ['UNITEST_build_DIR'])

	def __init__(self, node_name, template_name) :
		self.node_name = node_name
		if not (self.kcg_dir / self.node_name / "scade_type.h").is_file() :
			node_lst = '\n'.join(pth.parent.name for pth in self.kcg_dir.rglob('*/scade_type.h'))
			raise FileNotFoundError(f"unknown node name, please select one among the following:\n{node_lst}")
		
		self.template_name = template_name
		if not (self.template_dir / self.template_name / "scade_type.h").is_file() :
			template_lst = '\n'.join(pth.parent.name for pth in self.kcg_dir.rglob('*/Makefile'))
			raise FileNotFoundError(f"unknown template name, please select one among the following:\n{template_lst}")

		self.model_dir = self.build_dir / self.node_name
		self.model_dir.make_dirs()
		(self.model_dir / "src").make_dirs()
		(self.model_dir / "include").make_dirs()

	def prepare(self) :
		self.copy_node()
		self.copy_template()

	def copy_node(self) :
		src_dir = self.kcg_dir / self.node_name

		for i, d in [('*.c', 'src'), ('*.h', 'include')] :
			dst_dir = self.build_dir / self.node_name / d / "scade"
			dst_dir.delete()
			dst_dir.make_dirs()
			for src_pth in src_dir.glob(i) :
				dst_pth = dst_dir / src_pth.name
				scade_copy(src_pth, dst_pth)

	def copy_template(self) :
		for sub in (self.template_dir / self.template_name) :
			if (self.template_dir / self.template_name / sub).is_dir() :
				shutil.copytree(self.template_dir / self.template_name, self.model_dir, dirs_exist_ok=True)
			if (self.template_dir / self.template_name / sub).is_file() :
				shutil.copy(self.template_dir / self.template_name / sub, self.model_dir, dirs_exist_ok=True)
