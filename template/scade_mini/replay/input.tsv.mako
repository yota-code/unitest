<%
import re

stack = list()
for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
	if re.match(r'^\*?_I[0-9]+_', line[1]) :
		ctype, member = scade_map.clean(line)
		stack.append(
			"_{0:03d}{1}_{2}".format(n, line[1].lstrip('*'), line[-2])
			if line[1].startswith('*') else
			"_{0:03d}{1}".format(n, line[-2])
		)
if not stack :
	stack = ['_dummy_input']
%>\
#${'\t'.join(stack)}