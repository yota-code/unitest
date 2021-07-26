<%
import re
stack = list()
value = list()
default_map = {
	'R': 0.0,
	'Z': 0,
	'N': 0
}
for n, line in enumerate(scade_map.walk(follow_pointers=True)) :
	if re.match(r'^\*?_I[0-9]+_', line[0]) :
		stack.append(f"{n:03d}_{line[-2].rstrip('*')}")
		value.append(str(default_map[scade_map.ctype_map[line[-1]][0]]))
%>\
#${'\t'.join(stack)}
${'\t'.join(value)}
${'\t'.join('.' for i in range(len(value)))}