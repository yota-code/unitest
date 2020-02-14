#include <stdlib.h>
#include <stdio.h>

#include "scade_types.h"
#include "${node_name}.h"

int main() {
	
	_C_${node_name} unitest_C_;
	_C_${node_name} * _C_ = & unitest_C_;
	size_t p = (size_t) & unitest_C_;
	
	printf("${node_name}\t%ld\n", sizeof(_C_${node_name}));
% for line in scade_map.walk('_C_' + node_name, follow_pointer=False) :
<% ctype, member = scade_map.clean(line) %>\
	% if not ctype.endswith('*') :
	printf("${member}\t${ctype}\t%ld\n", ((size_t) &(${member})) - p);
	% endif
% endfor
	
	return EXIT_SUCCESS;
}