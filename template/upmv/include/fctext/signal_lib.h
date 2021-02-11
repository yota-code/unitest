#ifndef INCLUDE_fctext_signal_lib_H
#define INCLUDE_fctext_signal_lib_H

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

real s_tbX_average(s_tbX_seg_T * seg, size_t n) ;

#ifndef m_s_tb3_average
#define m_s_tb3_average(cmd_dur, J) ( J = s_tbX_average( (s_tbX_seg_T *) & cmd_dur, 3 ) )
#endif /* m_s_tb3_average */

#endif /* INCLUDE_fctext_signal_lib_H */