#!/usr/bin/env python3

def deg_to_bam(x) :
	return int(x * (float(1 << 30) / 90.0)) & 0xFFFFFFFF
