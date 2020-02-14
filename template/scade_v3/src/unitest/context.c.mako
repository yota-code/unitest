<%
import re
%>\
#include "unitest/context.h"

_C_${node_name} unitest_C_ = {0};

% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=False)) :
	% if re.match(r'^\*_I[0-9]+_', line[1]) :
<% ctype, member = scade_map.clean(line) %>\
${line[-1].rstrip(' *')} unitest_C${line[-2].lstrip('*')} = {0};
	% endif
% endfor

int unitest__init__(_C_${node_name} * _C_) {

	% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=False)) :
		% if re.match(r'^\*_I[0-9]+_', line[1]) :
<% ctype, member = scade_map.clean(line) %>\
	${member} = & unitest_C${line[-2].lstrip('*')};
		% endif
	% endfor
	
	return EXIT_SUCCESS;
	
}
