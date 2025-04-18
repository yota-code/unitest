#include <stdlib.h>
#include <stdio.h>

#include <inttypes.h>
#include <stdint.h>

#include <string.h>

#include "scade/scade_types.h"

#include "${node}.h"

_C_${node} unitest_context = {0};

int main(int argc, char * argv[]) {

	printf("sizeof context: %" PRIuPTR "\n", sizeof(unitest_context));

	memset(& unitest_context, 0, sizeof(_C_${node}));

	return EXIT_SUCCESS; 

}