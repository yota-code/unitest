#!/usr/bin/env python3

from cc_pathlib import Path

import structarray

lat_src, lon_src, lat_dst, lon_dst, lat_ini, lon_ini, spd_ini, alt_ini, hdg_ini  = Path("input.tsv").load()[0]

line = {
	"type": "Feature",
	"geometry": {
		"type": "LineString",
		"coordinates": [
			[float(lon_src), float(lat_src)],
			[float(lon_dst), float(lat_dst)],
		]
	},
	"properties": {
		"name": "line",
	}
}


traj = {
	"type": "Feature",
	"geometry": {
		"type": "LineString",
		"coordinates": [
			[float(line[13]), float(line[12])] for line in Path("output.tsv").load()[1:]
		],
	},
	"properties": {
		"name": "traj",
	}
}

geo_json = {
	"type": "FeatureCollection",
	"features": [
		line,
		traj,
	]
}

Path("traj.json").save(geo_json)
