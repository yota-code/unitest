#!/usr/bin/env python3

import os
import re
import shutil

from cc_pathlib import Path

import xxhash

def copy_dir(src_dir, dst_dir, recurse=False, hidden=False, dry_run=True, delete=False) :
	d_lst = list()
	f_lst = list()
	for src_pth in src_dir.iterdir() :
		if src_pth.is_dir :
			d_lst.append(src_pth)
		if src_pth.is_file() :
			if src_pth.name.startswith('.') and not hidden :
				continue
			dst_pth = dst_dir / src_pth.relative_to(src_dir)
			if dry_run :
				print(f"{src_pth} -> {dst_pth}")
			else :
				shutil.copy(src_pth, dst_pth)


class UnitestPrepare() :
	def __init__(self, node) :
		self.u_dir = Path(os.environ["UNITEST_root_DIR"]).resolve()
		self.w_dir = Path(os.environ["UNITEST_working_DIR"]).resolve()

		self.node = node

		print(self.u_dir, self.node)

		self.k_dir = self.u_dir / "kcg" / self.node
		self.t_dir = self.w_dir / "template"
		self.m_dir = self.w_dir / "model" / self.node

		self.w_dir.run('rsync', "-av", "--exclude", ".git", "--checksum", f"{self.t_dir}/", self.m_dir)

		self.copy_scade()
		self.tweak_scade()
		self.deconst_extern()

		# self.copy_fctext()
		self.prepare_typeguard()

		self.map_context()
		self.unroll_template()

		# self.map_it("input", node=self.node, meta=self.meta)

		self.compile_project()

	# def scan_include(self) :
	# 	self.i_lst = ["-I../include",]
	# 	self.i_lst += [f"-I../{root.relative_to(self.m_dir)}" for root, dirs, files in (self.m_dir / "include").walk()]

	def gcc_call(self) :
		g_lst = ["gcc", "-std=c11", "-g"]
		if os.environ.get("FORCE_ARCH_32", 0) != 0 :
			g_lst.append("-m32")
		g_lst.append("-I../include")
		g_lst += [f"-I../{root.relative_to(self.m_dir)}" for root, dirs, files in (self.m_dir / "include").walk()]
		return g_lst

	def copy_scade(self) :
		src_dir = (self.m_dir / "src" / "scade").make_dirs()
		inc_dir = (self.m_dir / "include" / "scade").make_dirs()

		src_dir.delete_content()
		inc_dir.delete_content()

		for ext, dst in [("*.h", inc_dir), ("*.c", src_dir)] :
			for pth in self.k_dir.glob(ext) :
				ret = self.k_dir.run("gcc", "-fpreprocessed", "-dD", "-E", "-P", pth)
				(dst / pth.name).write_text(ret.stdout.decode('utf8'))

		(inc_dir / f"{self.node}_extern.h").touch()

	def copy_fctext(self) :
		src_dir = (self.m_dir / "src" / "fctext").make_dirs()
		inc_dir = (self.m_dir / "include" / "fctext").make_dirs()

		self.w_dir.run('rsync', "-av", "--checksum", "--delete", '--prune-empty-dirs', f"{self.t_dir}/src/fctext/", src_dir)
		self.w_dir.run('rsync', "-av", "--checksum", "--delete", '--prune-empty-dirs', f"{self.t_dir}/include/fctext/", inc_dir)

		# copy_dir(self.t_dir, self.m_dir, dry_run=False)

	def unroll_template(self) :
		# from unitest.macco import unroll_folder
		import mako.template

		for src_pth in self.m_dir.rglob('*.mako') :
			if src_pth.name.startswith('.') :
				continue
			
			dst_pth = src_pth.with_suffix('')
			print(f"{src_pth.relative_to(self.w_dir)} -> {dst_pth.relative_to(self.w_dir)}")

			m = mako.template.Template(filename=str(src_pth), module_directory=str(self.w_dir / '.mako_tmp'))
			dst_pth.write_text(m.render(meta=self.meta, node=self.node))

			src_pth.unlink()

		# unroll_folder(self.t_dir, self.m_dir, arg)

	def deconst_extern(self) :
		if not (self.t_dir / ".deconst_extern.tsv").is_file() :
			return

		v_set = {line[0] for line in (self.t_dir / ".deconst_extern.tsv").load()}

		pth = self.m_dir / "include" / "scade" / f"{self.node}_extern.h"

		s_lst = list()
		for line in pth.read_text().splitlines() :
			token = line.split()[-1].rstrip(';')
			s_lst.append(line.replace('extern const ', 'extern ') if token in v_set else line)

		pth.write_text('\n'.join(s_lst))

	def tweak_scade(self) :
		print(f">>> PREPARE :: \x1b[35mtweak_scade_types\x1b[0m ()")

		scade_types_pth = self.m_dir / "include" / "scade" / "scade_types.h"
		scade_tweak_pth = self.t_dir / ".scade_tweak.tsv"

		t_lst = scade_types_pth.load().splitlines()

		if scade_tweak_pth.is_file() :
			for i, t in enumerate(t_lst) :
				for line in scade_tweak_pth.load() :
					if line[0].strip() == t.strip() :
						if len(line) == 1 :
							t_lst[i] = f'/* DEL {t} */'
							print(f'DEL {line[0]}')
						elif len(line) == 2 :
							t_lst[i] = f'{line[1]} /* UPD {t} */'
							print(f'UPD {line[0]} -> {line[1]}')
			
		scade_types_pth.write_text('\n'.join(t_lst))

	def compile_project(self) :
		self.m_dir.run("make")

	# def map_context(self) :
	# 	from unitest.macco import unroll_file

	# 	unroll_file(self.u_dir / "data", "node_context.c.mako", self.m_dir / "mapping", {"node": self.node})

	# 	cmd = self.gcc_call() + ["node_context.c", "-o", "node_context.exe"]

	# 	ret = (self.m_dir / "mapping").run(* cmd)
	# 	if ret.returncode != 0 :
	# 		raise ValueError("node_context.c couldn't compile properly")

	# 	ret = (self.m_dir / "mapping").run("./node_context.exe")
	# 	if ret.returncode != 0 :
	# 		raise ValueError("error launching node_context.exe")

	# 	from structarray.parself import ElfParser

	# 	self.meta = ElfParser(self.m_dir / "mapping" / "node_context.exe")
	# 	self.meta.run('context', self.m_dir / "mapping" / "context_map.tsv")

	def map_context(self) :
		from unitest.macco import unroll_file

		fnm = "node_context"

		unroll_file(self.u_dir / "data", f"{fnm}.c.mako", self.m_dir / "mapping", {'node': self.node})

		cmd = self.gcc_call() + [f"{fnm}.c", "-o", f"{fnm}.exe"]

		ret = (self.m_dir / "mapping").run(* cmd)
		if ret.returncode != 0 :
			raise ValueError(f"{fnm}.c couldn't compile properly")

		ret = (self.m_dir / "mapping").run(f"./{fnm}.exe")
		if ret.returncode != 0 :
			raise ValueError(f"error launching {fnm}.exe")

		from structarray.parself2 import ElfParser

		e = ElfParser(self.m_dir / "mapping" / f"{fnm}.exe")


		self.meta = e.get_meta("node_context")

		pth = self.m_dir / "mapping" / "context_map.tsv"

		self.meta.dump(pth, False, False)
		hsh = xxhash.xxh3_64(pth.read_bytes()).intdigest()
		self.meta.version = f"{hsh:016X}"

		hlk = pth.with_suffix(f".{hsh:016X}.tsv")
		if not hlk.is_file() :
			hlk.hardlink_to(pth)

	def map_it(self, n, ** arg) :
		from unitest.macco import unroll_file

		unroll_file(self.u_dir / "data", f"node_{n}.c.mako", self.m_dir / "mapping", arg)

		cmd = self.gcc_call() + [f"node_{n}.c", "-o", f"node_{n}.exe"]

		ret = (self.m_dir / "mapping").run(* cmd)
		if ret.returncode != 0 :
			raise ValueError(f"node_{n}.c couldn't compile properly")

		ret = (self.m_dir / "mapping").run(f"./node_{n}.exe")
		if ret.returncode != 0 :
			raise ValueError(f"error launching node_{n}.exe")

		from structarray.parself2 import ElfParser

		u = ElfParser(self.m_dir / "mapping" / f"node_{n}.exe")
		u.run(f"unitest_{n}", self.m_dir / "mapping" / f"{n}_map.tsv")

		return u

	def prepare_typeguard(self) :
		print(f">>> PREPARE :: \x1b[35mprepare_typedef\x1b[0m")

		typedef_rec = re.compile(r"typedef\s+(?P<old>.*?)\s+(?P<new>[a-zA-Z_][a-zA-Z0-9_]*)\s*;")

		txt = (self.m_dir / 'include' / 'scade' / 'scade_types.h').read_text()

		s_lst = [
			'#ifndef INCLUDE_fctext_scade_typeguard_H',
			'#define INCLUDE_fctext_scade_typeguard_H',
			''
		]

		for res in typedef_rec.finditer(txt) :
			s_lst.append(f"#define SCADE_TYPEGUARD_{res.group('new')}")

		s_lst.append('')
		s_lst.append('#endif /* INCLUDE_fctext_scade_typeguard_H */')

		(self.m_dir / 'include' / 'fctext' / 'scade_typeguard.h').write_text('\n'.join(s_lst))
	