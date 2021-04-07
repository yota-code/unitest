
#include "fctext/config_types.h"
#include "scade/model_extern.h"

#include "fctext/math_lib.h"
#include "fctext/signal_lib.h"


#ifdef DISABLED_CODE

real s_tbX_average(s_tbX_seg_T * seg, size_t n) {

	real t = 0.0;
	real s = 0.0;

	for (size_t i=0 ; i<n ; i++) {
		real cmd = seg[i].cmd;
		real dur = seg[i].dur;
		if ( (t + dur) <= T_CYCLE ) {
			s += cmd * dur;
		} else {
			s += cmd * m_BOUND((T_CYCLE - t), 0.0, T_CYCLE);
		}
		t += dur;
	}

	return s * F_CYCLE;

}

#endif