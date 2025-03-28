#!/usr/bin/env python3

import os
import re

from cc_pathlib import Path

class UnitestPrepare() :
	def __init__(self, node) :
		self.u_dir = Path(os.environ["UNITEST_root_DIR"]).resolve()
		self.w_dir = Path(os.environ["UNITEST_working_DIR"]).resolve()

		self.node = node

		self.m_dir = self.w_dir / "model" / self.node
		self.k_dir = self.w_dir / "kcg" / self.node
		self.t_dir = self.w_dir / "template"

		self.copy_scade()
		self.tweak_scade()

		self.copy_fctext()
		self.prepare_typedef()

		self.map_context()

		self.unroll_unitest()

	def gcc_call(self) :
		g_lst = ["gcc", "-std=c11", "-g"]
		if os.environ.get("FORCE_ARCH_32", 0) != 0 :
			g_lst.append("-m32")
		g_lst += ["-I../include", "-I../include/scade", "-I../include/fctext"]
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

	def copy_fctext(self) :
		src_dir = (self.m_dir / "src" / "fctext").make_dirs()
		inc_dir = (self.m_dir / "include" / "fctext").make_dirs()

		self.w_dir.run('rsync', "-av", "--checksum", "--delete", '--prune-empty-dirs', f"{self.t_dir}/src/fctext/", src_dir)
		self.w_dir.run('rsync', "-av", "--checksum", "--delete", '--prune-empty-dirs', f"{self.t_dir}/include/fctext/", inc_dir)

	def unroll_unitest(self) :
		from unitest.macco import unroll_folder

		src_dir = (self.m_dir / "src" / "fctext").make_dirs()
		inc_dir = (self.m_dir / "include" / "fctext").make_dirs()

		arg = {
			'meta' : self.meta,
			'node' : self.node
		}

		unroll_folder(self.t_dir / "src"/ "unitest", self.m_dir / "src" / "unitest", arg)
		unroll_folder(self.t_dir / "include"/ "unitest", self.m_dir / "include" / "unitest", arg)

	def tweak_scade(self) :
		print(f">>> PREPARE :: \x1b[35mtweak_scade_types\x1b[0m ()")

		scade_types_pth = self.m_dir / "include" / "scade" / "scade_types.h"
		scade_tweak_pth = self.t_dir / "scade_tweak.tsv"

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

	def map_context(self) :
		from unitest.macco import unroll_file

		unroll_file(self.u_dir / "data", "node_context.c.mako", self.m_dir / "mapping", {"node": self.node})

		cmd = self.gcc_call() + ["node_context.c", "-o", "node_context.exe"]

		ret = (self.m_dir / "mapping").run(* cmd)
		if ret.returncode != 0 :
			raise ValueError("node_context.c couldn't compile properly")

		ret = (self.m_dir / "mapping").run("./node_context.exe")
		if ret.returncode != 0 :
			raise ValueError("error launching node_context.exe")

		from structarray.parself import ElfParser

		self.meta = ElfParser(self.m_dir / "mapping" / "node_context.exe")
		self.meta.run('context', self.m_dir / "mapping" / "context_map.tsv")

	def map_interface(self) :
		cwd = self.mapping_dir
		cwd.make_dirs()

		(cwd / 'structarray_interface.c').write_text(scade_interface_template)

		cmd = self.gcc_lst + ["structarray_interface.c", "-o", "structarray_interface.exe"]

		ret = cwd.run(* cmd)
		if ret.returncode != 0 :
			raise ValueError("gcc couldn't compile properly")

		ret = cwd.run("./structarray_interface.exe")

		for k in ["input", "output"] :
			u = structarray.StructInfo(cwd / 'structarray_interface.exe')
			u.parse(k)
			u.save(cwd / f"{k}.json")

	def prepare_typedef(self) :
		print(f">>> PREPARE :: \x1b[35mprepare_typedef\x1b[0m")

		typedef_rec = re.compile(r"typedef\s+(?P<old>.*?)\s+(?P<new>[a-zA-Z_][a-zA-Z0-9_]*)\s*;")

		txt = (self.m_dir / 'include' / 'scade' / 'scade_types.h').read_text()

		s_lst = [
			'#ifndef INCLUDE_fctext_scade_typedef_H',
			'#define INCLUDE_fctext_scade_typedef_H',
			''
		]

		for res in typedef_rec.finditer(txt) :
			s_lst.append(f"#define SCADE_TYPEDEF_{res.group('new')}")

		s_lst.append('')
		s_lst.append('#endif /* INCLUDE_fctext_scade_typedef_H */')

		(self.m_dir / 'include' / 'fctext' / 'scade_typedef.h').write_text('\n'.join(s_lst))
	