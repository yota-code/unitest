<%
import re
%>\
% for n, line in enumerate(scade_map.walk(follow_pointers=True)) :
	% if re.match(r'^\*?_I[0-9]+_', line[0]) :
${f'{n:03d}'}_${line[-2].rstrip('*')}	${scade_map.ctype_map[line[-1]]}
	%endif
%endfor