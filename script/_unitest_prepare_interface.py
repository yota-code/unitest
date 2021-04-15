#!/usr/bin/env python3

import os
import sys

from cc_pathlib import Path

import structarray
import structarray.tools

import unitest

if __name__ == '__main__' :
	
	node_name = sys.argv[1]
	template_name = sys.argv[2]
	
	node_dir = Path(os.environ['UNITEST_build_DIR']) / node_name
	if not node_dir.is_dir() :
		raise ValueError("Not a valid directory:{0}".format(node_dir))

	scade_map = structarray.tools.scade_map_context(
		node_dir / "mapping",
		node_name,
		[ "../include/scade", "../include/fctext", "../include" ]
	)
	
	template_dir = Path(os.environ['UNITEST_template_DIR']) / template_name
	unitest.unroll_template_folder(template_dir, node_dir, {
		'scade_map' : scade_map,
		'node_name' : node_name
	})
