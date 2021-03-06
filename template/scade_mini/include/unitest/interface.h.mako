<%
import re

ctype_map = {
	'real' : 'float',
	'boolean' : 'int8_t',
	'integer' : 'int32_t',
	'pointer' : 'void *',
}
%>\
#ifndef INCLUDE_unitest_interface_H
#define INCLUDE_unitest_interface_H

#include <inttypes.h>

#include "unitest/context.h"

<% is_empty = True %>\
typedef struct {
% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
	% if re.match(r'^\*?_I[0-9]+_', line[1]) :
<%
ctype, member = scade_map.clean(line)
is_empty = False
%>\
		% if line[1].startswith('*') :
	${ctype_map[ctype]} _${'{0:03d}'.format(n)}${line[1].lstrip('*')}_${line[-2]};
		% else :
	${ctype_map[ctype]} _${'{0:03d}'.format(n)}${line[-2]};
		% endif
	% endif
% endfor
% if is_empty :
	int _dummy_input;
%endif
} unitest_input_T;

<% is_empty = True %>\
typedef struct {
% for n, line in enumerate(scade_map.walk('_C_' + node_name, follow_pointer=True)) :
	% if re.match(r'^\*?_O[0-9]+_', line[1]) :
<%
ctype, member = scade_map.clean(line)
is_empty = False
%>\
	${ctype_map[ctype]} _${'{0:03d}'.format(n)}_${line[-2]};
	% endif
% endfor
% if is_empty :
	int _dummy_input;
%endif
} unitest_output_T;

extern unitest_input_T unitest_input;
extern unitest_output_T unitest_output;

int unitest_set_input(_C_${node_name} * _C_) ;
int unitest_get_output(_C_${node_name} * _C_) ;

#endif /* INCLUDE_unitest_interface_H */
