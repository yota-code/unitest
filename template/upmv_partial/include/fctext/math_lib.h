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

#define m_m_bound_up(x, upper_bound, y) { y = m_BOUND_UP(x, upper_bound); }
#define m_m_bound_low(x, lower_bound, y) { y = m_BOUND_LOW(x, upper_bound); }
#define m_m_bound(x, lower_bound, upper_bound, y) { y = m_BOUND(x, lower_bound, upper_bound); }

#define m_m_mod_N(a, m, n) { n = (((a % m) < 0) ? ((a % m) + m) : (a % m)); }

#ifdef SCADE_64BIT_REAL

	#define m_m_abs(x, abs_x) { abs_x = fabs(x); }
	#define m_m_sqrt(x, sqrt_x) { sqrt_x = sqrt(x); }

	#define m_m_cos(a, cos_a) { cos_a = cos(a); }
	#define m_m_acos(x, acos_x) { acos_x = acos(x); }
	#define m_m_sin(a, sin_a) { sin_a = sin(a); }
	#define m_m_asin(x, asin_x) { asin_x = asin(x); }
	#define m_m_tan(a, tan_a) { tan_a = tan(a); }
	#define m_m_atan(x, atan_x) { atan_x = atan(x); }

	#define m_m_atan2(y, x, atan2_y_x) { atan2_y_x = atan2(y, x); }

	#define m_m_sincos(a, sin_a, cos_a) { \
		sin_a = sin(a); \
		cos_a = cos(a); \
	}

	#define m_m_copysign(m, s, y) { y = copysign(m, s); }

	#define m_m_ceil(x, n) { n = (_int)( m_BOUND(ceil(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_floor(x, n) { n = (_int)( m_BOUND(floor(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_round(x, n) { n = (_int)( m_BOUND(round(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }

#else

	#define m_m_abs(x, abs_x) { abs_x = fabsf(x); }
	#define m_m_sqrt(x, sqrt_x) { sqrt_x = sqrtf(x); }

	#define m_m_cos(a, cos_a) { cos_a = cosf(a); }
	#define m_m_acos(x, acos_x) { acos_x = acosf(x); }
	#define m_m_sin(a, sin_a) { sin_a = sinf(a); }
	#define m_m_asin(x, asin_x) { asin_x = asinf(x); }
	#define m_m_tan(a, tan_a) { tan_a = tanf(a); }
	#define m_m_atan(x, atan_x) { atan_x = atanf(x); }

	#define m_m_atan2(y, x, atan2_y_x) { atan2_y_x = atan2f(y, x); }

	#define m_m_sincos(a, sin_a, cos_a) { \
		sin_a = sinf(a); \
		cos_a = cosf(a); \
	}

	#define m_m_copysign(m, s, y) { y = copysignf(m, s); }

	#define m_m_ceil(x, n) { n = (_int)( m_BOUND(ceilf(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_floor(x, n) { n = (_int)( m_BOUND(floorf(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_round(x, n) { n = (_int)( m_BOUND(roundf(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }

#endif

#define m_m_divide(a, b, r) ( r = ( (b == 0.0) ? ((a >= 0) ? (INFINITY) : (-INFINITY)) : (a / b) ))

#define m_BAM_to_DEG ( ((double)(90.0)) / ((double)(1 << 30)) )
#define m_DEG_to_BAM ( ((double)(1 << 30)) / ((double)(90.0)) )

#define m_BAM_to_RAD ( ((double)(M_PI_2)) / ((double)(1 << 30)) )
#define m_RAD_to_BAM ( ((double)(1 << 30)) / ((double)(M_PI_2)) )

#define m_RAD_to_DEG ( ((double)(90.0)) / ((double)(M_PI_2)) )
#define m_DEG_to_RAD ( ((double)(M_PI_2)) / ((double)(90.0)) )

#define m_m_bam_to_deg_U(bam, deg) ( deg = ( ((real)((uint32_t)(bam))) * m_BAM_to_DEG ) )
#define m_m_bam_to_deg_S(bam, deg) ( deg = ( ((real)((int32_t)(bam))) * m_BAM_to_DEG ) )
#define m_m_deg_to_bam(rad, bam) ( bam = ( (int32_t)( ((double)(deg)) * m_DEG_to_BAM )) )

#define m_m_bam_to_rad_U(bam, rad) ( rad = ( ((real)((uint32_t)(bam))) * m_BAM_to_RAD ) )
#define m_m_bam_to_rad_S(bam, rad) ( rad = ( ((real)((int32_t)(bam))) * m_BAM_to_RAD ) )
#define m_m_rad_to_bam(rad, bam) ( bam = ( (int32_t)( ((double)(rad)) * m_RAD_to_BAM )) )

#define m_m_deg_to_rad(deg, rad) ( rad = ( deg * m_DEG_to_RAD ) ) 
#define m_m_rad_to_deg(rad, deg) ( deg = ( rad * m_RAD_to_DEG ) )

#endif /* INCLUDE_fctext_math_lib_H */