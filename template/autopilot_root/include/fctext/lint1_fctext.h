#ifndef _INCLUDE_SCADE_TYPES
#    include "scade_types.h"
#endif

#define _INCLUDE_lint1

typedef struct {
	real R_dummy;
} table1;

typedef struct {
	real _I0_The_Input;
	table1 * _I1_The_Table;
	real _O0_The_Output;
} _C_lint1;

void lint1_init (_C_lint1 * C);

void lint1 (_C_lint1 * C);
