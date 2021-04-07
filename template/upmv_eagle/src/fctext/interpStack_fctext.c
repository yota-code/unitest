#include "fctext/interpStack_fctext.h"

#include <float.h>
#include <stdio.h>

int cptError = 0;

void interpStack_init (_C_interpStack * C) {

	circular_interp__init__(& (C->stack));

}

void interpStack (_C_interpStack * C) {

	circular_interp_push(& (C->stack), C->_I0_push_time, C->_I1_push_value);
	circular_interp__debug__(& (C->stack), C->_I2_get_time);

}
