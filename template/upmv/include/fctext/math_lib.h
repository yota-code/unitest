#ifndef INCLUDE_fctext_math_lib_H
#define INCLUDE_fctext_math_lib_H

#include <math.h>

#define m_BOUND_UP(x, upper_bound) ( ((upper_bound < x) ? (upper_bound) : (x)) )
#define m_BOUND_LOW(x, lower_bound) ( ((x < lower_bound) ? (lower_bound) : (x)) )
#define m_BOUND(x, lower_bound, upper_bound) (\
	(lower_bound <= upper_bound) ? (\
		m_BOUND_LOW( m_BOUND_UP(x, upper_bound), lower_bound )\
	) : ((lower_bound + upper_bound) / 2.0)\
)

#ifndef m_m_abs
#define m_m_abs(x, y) ( y = fabsf(x) )
#endif				

#ifndef m_m_sqrt
#define m_m_sqrt(x, y) ( y = sqrtf(x) )
#endif				

#ifndef m_m_copysign
#define m_m_copysign(magnitude, sign, result) ( result = copysignf(magnitude, sign) )
#endif

#ifndef m_m_bound_up
#define m_m_bound_up(x, upper_bound, y) ( y = m_BOUND_UP(x, upper_bound) )
#endif

#ifndef m_m_bound_low
#define m_m_bound_low(x, lower_bound, y) ( y = m_BOUND_LOW(x, upper_bound) )
#endif

#ifndef m_m_bound
#define m_m_bound(x, lower_bound, upper_bound, y) ( y = m_BOUND(x, lower_bound, upper_bound) )
#endif

#endif /* INCLUDE_fctext_math_lib_H */