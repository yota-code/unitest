<%
import re
%>\
% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
	% if re.match(r'^\*?_O[0-9]+_', line[1]) :
<% ctype, member = scade_map.clean(line) %>\
_${'{0:03d}'.format(n)}${line[-2]}	${ctype}
	% endif
% endfor