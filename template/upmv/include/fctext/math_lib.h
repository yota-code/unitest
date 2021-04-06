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

#define m_m_bound_up(x, upper_bound, y) ( y = m_BOUND_UP(x, upper_bound) )
#define m_m_bound_low(x, lower_bound, y) ( y = m_BOUND_LOW(x, upper_bound) )
#define m_m_bound(x, lower_bound, upper_bound, y) ( y = m_BOUND(x, lower_bound, upper_bound) )

#define m_m_mod_N(a, m, n) ( n = ((a % m) < 0) ? ((a % m) + m) : (a % m) )

#ifdef SCADE_64BIT_REAL

	#define m_m_abs(x, y) ( y = fabs(x) )
	#define m_m_sqrt(x, y) ( y = sqrt(x) )

	#define m_m_cos(x, y) ( y = cos(x) )
	#define m_m_acos(x, y) ( y = acos(x) )
	#define m_m_sin(x, y) ( y = sin(x) )
	#define m_m_asin(x, y) ( y = asin(x) )
	#define m_m_tan(x, y) ( y = tan(x) )
	#define m_m_atan(x, y) ( y = atan(x) )

	#define m_m_copysign(m, s, y) ( y = copysign(m, s) )

	#define m_m_ceil(x, n) ( n = (_int)( m_BOUND(ceil(x), SCADE_INT_MIN, SCADE_INT_MAX) ) )
	#define m_m_floor(x, n) ( n = (_int)( m_BOUND(floor(x), SCADE_INT_MIN, SCADE_INT_MAX) ) )
	#define m_m_round(x, n) ( n = (_int)( m_BOUND(round(x), SCADE_INT_MIN, SCADE_INT_MAX) ) )

#else

	#define m_m_abs(x, y) ( y = fabsf(x) )
	#define m_m_sqrt(x, y) ( y = sqrtf(x) )

	#define m_m_cos(x, y) ( y = cosf(x) )
	#define m_m_acos(x, y) ( y = acosf(x) )
	#define m_m_sin(x, y) ( y = sinf(x) )
	#define m_m_asin(x, y) ( y = asinf(x) )
	#define m_m_tan(x, y) ( y = tanf(x) )
	#define m_m_atan(x, y) ( y = atanf(x) )

	#define m_m_copysign(m, s, y) ( y = copysignf(m, s) )

	#define m_m_ceil(x, n) ( n = (_int)( m_BOUND(ceilf(x), SCADE_INT_MIN, SCADE_INT_MAX) ) )
	#define m_m_floor(x, n) ( n = (_int)( m_BOUND(floorf(x), SCADE_INT_MIN, SCADE_INT_MAX) ) )
	#define m_m_round(x, n) ( n = (_int)( m_BOUND(roundf(x), SCADE_INT_MIN, SCADE_INT_MAX) ) )

#endif

#define m_m_bam_to_deg_U(bam, deg) ( deg = ( 90.0 * ( ((real)((uint32_t)(bam))) / 1073741824.0 ) ) )
#define m_m_bam_to_deg_S(bam, deg) ( deg = ( 90.0 * ( ((real)((int32_t)(bam))) / 1073741824.0 ) ) )

#define m_m_bam_to_rad_U(bam, rad) ( deg = ( M_PI_2 * ( ((real)((uint32_t)(bam))) / 1073741824.0 ) ) )
#define m_m_bam_to_rad_S(bam, rad) ( deg = ( M_PI_2 * ( ((real)((int32_t)(bam))) / 1073741824.0 ) ) )

#define m_m_deg_to_rad(deg, rad) ( rad = ( (M_PI_2 / 90.0) * deg ) ) 
#define m_m_rad_to_deg(rad, deg) ( deg = ( (90.0 / M_PI_2) * rad  ) ) 

#endif /* INCLUDE_fctext_math_lib_H */