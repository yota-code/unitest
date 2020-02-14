<%
import re

is_empty = True
%>\
% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
	% if re.match(r'^\*?_I[0-9]+_', line[1]) :
<%
ctype, member = scade_map.clean(line)
is_empty = False
%>\
		% if line[1].startswith('*') :
_${'{0:03d}'.format(n)}${line[1].lstrip('*')}_${line[-2]}	${ctype}
		% else :
_${'{0:03d}'.format(n)}${line[-2]}	${ctype}
		% endif
	% endif
% endfor
% if is_empty :
_xxx_dummy_input	real
% endif
