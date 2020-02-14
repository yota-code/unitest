#include "fctext/lint1_fctext.h"

#include "fctext/linear_interpolation.h"

void lint1_init(_C_lint1 * C) {
	// do nothing
}

void lint1(_C_lint1 * C) {
	C->_O0_The_Output = lint20((lint20_C *) (C->_I1_The_Table), C->_I0_The_Input);
}
