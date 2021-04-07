#ifndef INCLUDE_fctext_interpStack_H
#define INCLUDE_fctext_interpStack_H

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

#include "fctext/circular_interp.h"

typedef struct {
	_int _I0_push_time;
	Vec3 * _I1_push_value;
	_int _I2_get_time;
	Vec3 _O0_return_value;
	circular_interp_T stack;
} _C_interpStack;

void interpStack_init(_C_interpStack * C);
void interpStack(_C_interpStack * C);

#endif /* INCLUDE_fctext_interpStack_H */