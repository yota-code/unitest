#include <assert.h>
#include <string.h>

#include "t_tb3_fctext.h"

#include "traj_lib.h"

void t_tb3_init(_C_t_tb3 * C) {
	static_assert( sizeof(t_tb3_C) == sizeof(tb3_C), "probable structure missmatch: sizeof(_C_t_tb3) == sizeof(tb3_C)");

	memset(C, 0, sizeof(_C_t_tb3));
}

void t_tb3(_C_t_tb3 * C) {
	tb3__auto__(
		(tb3_C *)( &(C->_O0_tb3_obj) ),	C->_I4_jm, C->_I5_am, C->_I0_a0, C->_I1_s0, C->_I2_ag, C->_I3_sg
	);
}

