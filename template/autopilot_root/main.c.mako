#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "unitest/interface.h"
#include "unitest/loop.h"

int main(int argc, char * argv[]) {

	FILE * input_fid = NULL;
	FILE * full_fid = NULL;
	FILE * output_fid = NULL;
	
	unitest__init__(& unitest_C_);
	
	${node_name}_init(& unitest_C_);

	input_fid = fopen("input.reb", "rb"); // binary file of the inputs
	full_fid = fopen("full.reb", "wb"); // binary file of the whole structure
	output_fid = fopen("output.reb", "wb"); // binary file of the ouputs
		
	if ( input_fid != NULL && full_fid != NULL && output_fid != NULL ) {
		while ( fread(& unitest_input, 1, sizeof(unitest_input_T), input_fid) == sizeof(unitest_input_T) ) {
			
			unitest_loop(& unitest_C_);
			
			unitest_set_input(& unitest_C_);
			
			${node_name}(& unitest_C_);
			
			unitest_get_output(& unitest_C_);
		
			fwrite(& unitest_C_, sizeof(_C_${node_name}), 1, full_fid);
			fwrite(& unitest_output, sizeof(unitest_output_T), 1, output_fid);
			
		}
	} else {
		printf("ERROR:can not open the replay files\n");
	}
	
	if ( input_fid != NULL ) { fclose(input_fid); }
	if ( full_fid != NULL ) { fclose(full_fid); }
	if ( output_fid != NULL ) { fclose(output_fid); }
	
	return EXIT_SUCCESS;

}
