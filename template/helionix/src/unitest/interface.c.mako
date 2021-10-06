<%
import re
%>\
#include <stdlib.h>

#include "unitest/interface.h"
% for w in ['input', 'output'] :

unitest_${w}_T unitest_${w} = {0};

int unitest_interface_${w}(_C_${node_name} * _C_) {

	% for n, line in enumerate(scade_map.walk(follow_pointers=True)) :
		% if re.match(r'^\*?_' + w[0].upper() + r'[0-9]+_', line[0]) :
<%
path = '.'.join(line[:-1]).replace('*.', '->')
%>\
% if w == "input" :
	_C_->${path} = unitest_${w}._${f'{n:03d}'}_${line[-2].rstrip('*')};
%elif w == "output" :
	unitest_${w}._${f'{n:03d}'}_${line[-2].rstrip('*')} = _C_->${path};
%endif
		%endif
%endfor

 	return EXIT_SUCCESS;

}
%endfor
