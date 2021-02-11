
#include "fctext/config_types.h"
#include "scade/model_extern.h"

#include "fctext/math_lib.h"
#include "fctext/signal_lib.h"

real s_tbX_average(s_tbX_seg_T * seg, size_t n) {

	real t = 0.0;
	real s = 0.0;

	for (size_t i=0 ; i<n ; i++) {
		real cmd = seg[i].cmd;
		real dur = seg[i].dur;
		if ( (t + dur) <= period ) {
			s += cmd * dur;
		} else {
			s += cmd * m_BOUND((period - t), 0.0, period);
		}
		t += dur;
	}

	return s / period;

}
