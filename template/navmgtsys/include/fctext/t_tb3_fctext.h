#ifndef INCLUDE_t_tb3_fctext_H
#define INCLUDE_t_tb3_fctext_H

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

typedef struct {
	real _I0_a0;
	real _I1_s0;
	real _I2_ag;
	real _I3_sg;
	real _I4_jm;
	real _I5_am;
	t_tb3_C _O0_tb3_obj;
	/* Memories */

	// None

} _C_t_tb3;

void t_tb3_init(_C_t_tb3 * C);
void t_tb3(_C_t_tb3 * C);

#endif /* INCLUDE_t_tb3_fctext_H */
