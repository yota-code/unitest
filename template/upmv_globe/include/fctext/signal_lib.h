#ifndef INCLUDE_fctext_signal_lib_H
#define INCLUDE_fctext_signal_lib_H

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

#ifdef DISABLED_CODE
	real s_tbX_average(s_tbX_seg_T * seg, size_t n) ;
	
	#define m_s_tb3_average(cmd_dur, J) ( J = s_tbX_average( (s_tbX_seg_T *) & cmd_dur, 3 ) )
#endif

#endif /* INCLUDE_fctext_signal_lib_H */