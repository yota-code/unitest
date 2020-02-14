<%
import re
%>\
#include <stdlib.h>

#include "unitest/interface.h"

unitest_input_T unitest_input = {0};
unitest_output_T unitest_output = {0};

int unitest_set_input(_C_${node_name} * _C_) {

	% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
		% if re.match(r'^\*?_I[0-9]+_', line[1]) :
<% ctype, member = scade_map.clean(line) %>\
			% if line[1].startswith('*') :
	${member} = unitest_input._${'{0:03d}'.format(n)}${line[1].lstrip('*')}_${line[-2]};
			% else :
	${member} = unitest_input._${'{0:03d}'.format(n)}${line[-2]};
			% endif
		% endif
	% endfor
	
	return EXIT_SUCCESS;

}

int unitest_get_output(_C_${node_name} * _C_) {

	% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
		% if re.match(r'^\*?_O[0-9]+_', line[1]) :
<% ctype, member = scade_map.clean(line) %>\
	unitest_output._${'{0:03d}'.format(n)}_${line[-2]} = ${member};
		% endif
	% endfor
	
	return EXIT_SUCCESS;

}
