<%
import re
%>\
#ifndef INCLUDE_unitest_interface_H
#define INCLUDE_unitest_interface_H

#include <inttypes.h>

#include "unitest/context.h"

%for w in ['input', 'output'] :
typedef struct {
	% for n, line in enumerate(scade_map.walk(follow_pointers=True)) :
		% if re.match(r'^\*?_' + w[0].upper() + r'[0-9]+_', line[0]) :
	${line[-1]} _${f'{n:03d}'}_${line[-2].rstrip('*')};
	%endif
% endfor
} unitest_${w}_T;

extern unitest_${w}_T unitest_${w};

int unitest_interface_${w}(_C_${node_name} * _C_) ;

%endfor
#endif /* INCLUDE_unitest_interface_H */
