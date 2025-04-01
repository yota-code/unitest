#include <stdlib.h>
#include <stdio.h>

#include <stdint.h>

#include <string.h>

#include "unitest/interface.h"

unitest_input_T unitest_input = {0};
unitest_output_T unitest_output = {0};

int main(int argc, char * argv[]) {

	printf("sizeof input: %" PRIuPTR "\n", sizeof(unitest_input));
	printf("sizeof output: %" PRIuPTR "\n", sizeof(unitest_output));

	memset(& unitest_input, 0, sizeof(unitest_input));
	memset(& unitest_output, 0, sizeof(unitest_output));

	return EXIT_SUCCESS; 

}