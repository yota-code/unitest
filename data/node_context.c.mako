#include <stdlib.h>
#include <stdio.h>

#include <stdint.h>

#include <string.h>

#include "scade_types.h"

#include "${node}.h"

_C_${node} context = {0};

int main(int argc, char * argv[]) {

	printf("sizeof context: %" PRIuPTR "\n", sizeof(context));

	memset(& context, 0, sizeof(_C_${node}));

	return EXIT_SUCCESS; 

}