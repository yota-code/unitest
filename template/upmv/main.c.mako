#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "unitest/interface.h"

int main(int argc, char * argv[]) {

	FILE * input_fid = NULL;
	FILE * context_fid = NULL;
	FILE * output_fid = NULL;

<%
import re
%>\
% for n, (c, p, m) in enumerate(scade_map.tree[scade_map.var_type]) :
	% if re.match(r'^\*?_I[0-9]+_', m) and p :
	${c} _input${m.rstrip('*')} = {0};
	unitest_context.${m} = & (_input${m.rstrip('*')});
	%endif
%endfor
	
	unitest_init(& unitest_context);
	
	${node_name}_init(& unitest_context);

	input_fid = fopen("input.reb", "rb"); // binary file of the inputs
	context_fid = fopen("context.reb", "wb"); // binary file of the whole structure
	output_fid = fopen("output.reb", "wb"); // binary file of the ouputs
		
	if ( input_fid != NULL && context_fid != NULL && output_fid != NULL ) {
		while ( fread(& unitest_input, 1, sizeof(unitest_input_T), input_fid) == sizeof(unitest_input_T) ) {
			
			unitest_loop(& unitest_context);
			
			unitest_interface_input(& unitest_context);
			
			${node_name}(& unitest_context);
			
			unitest_interface_output(& unitest_context);
		
			fwrite(& unitest_context, sizeof(_C_${node_name}), 1, context_fid);
			fwrite(& unitest_output, sizeof(unitest_output_T), 1, output_fid);
			
		}
	} else {
		printf("ERROR:can not open the replay files\n");
	}
	
	if ( input_fid != NULL ) { fclose(input_fid); }
	if ( context_fid != NULL ) { fclose(context_fid); }
	if ( output_fid != NULL ) { fclose(output_fid); }
	
	return EXIT_SUCCESS;

}
